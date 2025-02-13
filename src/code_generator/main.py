#!/usr/bin/env python
from random import randint
from typing import Optional

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start,router,or_
import shutil

from code_generator.crews.api_parser.api_parser import ApiParser
from code_generator.crews.Model_Layer.Model_Layer import ModelLayer
from code_generator.crews.evaluate_api_parser.evaluate_api_parser import EvaluateApiParser
import requests
import zipfile
import os
import openai
import subprocess

# Load API key from environment variable
openai.api_key = os.getenv("OPEN_API_KEY")


class CodeGeneratorState(BaseModel):
    project_name: str = ""
    package_name: str = ""
    dependencies: str = ""
    java_version: int = 11
    language: str = ""
    build_type:str='maven'
    boot_version:str='3.3.0'
    base_url:str = "https://start.spring.io/starter.zip"
    api_result: dict = {}
    entity_result: dict = {}
    model_path: str = ""
    feedback:Optional[str]=""
    valid:bool=False
    retry_count:int=0
    build_output:Optional[str]=""
    
    


class CodeGenerator(Flow[CodeGeneratorState]):

    @start()
    def Intialization(self):
        print("Provide the details")
        self.state.project_name = input("Enter the project name: ")
        self.state.package_name = input("Enter the package name (default com.example): ")
        self.state.dependencies = input("Enter the dependencies (comma separated, e.g., web,jpa): ").split(',')
        self.state.java_version = input("Enter Java version (default 11): ") or '11'
        self.state.language = input("Enter language (java/kotlin, default java): ") or 'java'

    @listen(Intialization)
    def generate_spring_boot_project(self):
        params = {
            'type': f'{self.state.build_type}-project',
            'language': self.state.language,
            'javaVersion': self.state.java_version,
            'dependencies': ','.join(self.state.dependencies),
            'artifactId': self.state.project_name,
            'groupId': self.state.package_name,
            'bootVersion': self.state.boot_version
        }

        print(params)
        response = requests.get(self.state.base_url, params=params)
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.text)

        if response.status_code == 200:
            zip_file_path = f'{self.state.project_name}.zip'
            with open(f'{self.state.project_name}.zip', 'wb') as file:
                file.write(response.content)
            if not os.path.exists(self.state.project_name):
                os.makedirs(self.state.project_name)

            # Unzip the file into the specified folder
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(self.state.project_name)
            
            # Remove the original ZIP file after extracting
            os.remove(zip_file_path)
            print(f"Unzipped the project to: {self.state.project_name}")
            return f"Spring Boot project {self.state.project_name} created successfully!"
        else:
            return "Failed"
        

    @listen(generate_spring_boot_project)
    def configure_application_properties(self):
#         properties_content = """spring.datasource.url=jdbc:h2:mem:testdb
# spring.datasource.driverClassName=org.h2.Driver
# spring.datasource.username=sa
# spring.datasource.password=password
# spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
# spring.h2.console.enabled=true
# """
        properties_content = os.getenv("SPRING_BOOT_PROPERTIES", "")
    
        # Replace escape sequences with actual newlines
        properties_content = properties_content.replace("\\n", "\n")

        properties_file_path = os.path.join(self.state.project_name, "src", "main", "resources", "application.properties")

        if not os.path.exists(os.path.dirname(properties_file_path)):
            os.makedirs(os.path.dirname(properties_file_path))

        with open(properties_file_path, 'w') as file:
            file.write(properties_content)

        print(f"application.properties configured successfully at {properties_file_path}")



    @listen(or_(configure_application_properties,"retry"))
    def api_parser(self):
        print("parsing the api")
        result = (
            ApiParser()
            .crew()
            .kickoff(inputs={"feedback":self.state.feedback})
        )

        print("api result: ", result.raw)
        self.state.api_result = result.raw  # Save the result in state
        print("API parsed successfully and stored in state.")
    
    @router(api_parser)
    def evaluate_api(self):
        if self.state.retry_count >3:
            return "max_retry"
        # Evaluate the result of the API parser
        result=EvaluateApiParser().crew().kickoff(inputs={"api_result":self.state.api_result})
        self.state.valid=result["valid"]
        self.state.feedback=result["feedback"]
        
        print("valid",self.state.valid)
        print("feedback",self.state.feedback)
        self.state.retry_count+=1
        
        if self.state.valid:
            return "completed"
        return "retry"
    
    @router("max_retry")
    def max_retry_limit(self):
        print("reached the try limit proceding with the same one")
        return "completed"
    
    
    @router(or_("completed","buildfail"))
    def SpringBootApplication(self):
        print("Generating model")
        print("API Result: ", self.state.api_result)
        # Example base path
        base_path = os.path.join(os.path.abspath(self.state.project_name), "src", "main", "java")
        # Convert package name to directory path
        package_path = self.state.package_name.replace('.', os.sep)
        # Full path to the models directory
        models_path = os.path.join(base_path, package_path,self.state.project_name)
        print ("models_path",models_path)
        print(os.path.exists(models_path))
        if os.path.exists(models_path):
            print(f"Cleaning existing directory contents: {models_path}")
        
            # Delete only contents inside models_path, but not the folder itself
            for filename in os.listdir(models_path):
                file_path = os.path.join(models_path, filename)
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Delete subdirectories
            
        self.state.model_path = models_path
        print(f"Models directory path: {models_path}")
        kickoff_inputs = {
            'api_result': self.state.api_result,
            'project_name': self.state.project_name,
            'package_name': self.state.package_name,
            'models_path': models_path,
            'feedback':self.state.build_output
        }

        

        result = ModelLayer().crew().kickoff(inputs=kickoff_inputs)

        print("Model result: ", result.raw)
        self.state.entity_result = result.raw  # Save the result in state
        print("Entity Model successfully and stored in state.")
    
    @listen(SpringBootApplication)
    def build_and_run_springboot(self):
        try:
            project_directory = os.path.abspath(self.state.project_name)
            print(f"Project directory: {project_directory}")
            # Navigate to the Spring Boot project directory
            if os.path.exists(project_directory):
                os.chdir(project_directory)
                print("Directory exists:", os.listdir(project_directory))
            else:
                print("Directory does not exist:", project_directory)
                return
            
            # Build the project
            build_command = ["mvn", "clean", "package"]
            build_process=subprocess.run(build_command,stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
            if build_process.returncode == 0:
                print("Build Success!")
            else:
                self.state.build_output=build_process.stdout.decode()
                print("Build Output:", self.state.build_output)
                return "buildfail"

            # Run the built JAR file
            jar_file = f"target/{self.state.project_name}-0.0.1-SNAPSHOT.jar"  # Adjust according to your project
            run_command = ["java", "-jar", jar_file]
            subprocess.Popen(run_command,shell=True)

            print("Spring Boot application is running...")
        except subprocess.CalledProcessError as e:
            print(f"Error during build or execution: {e}")
        except FileNotFoundError as e:
            print(f"Directory not found: {project_directory}. Please check the path.")
        except Exception as e:
            print(f"Unexpected error: {e}")


def kickoff():
    poem_flow = CodeGenerator()
    poem_flow.kickoff()


def plot():
    poem_flow = CodeGenerator()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()

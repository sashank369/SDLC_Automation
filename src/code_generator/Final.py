#!/usr/bin/env python
from random import randint
from typing import Optional

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start,router,or_



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
    count:int=0
    
    


class CodeGenerator(Flow[CodeGeneratorState]):

    @start()
    def Intialization(self):
        print("First Function")



    @listen(Intialization)
    def api_parser(self):
        print("API Parser",self.state.project_name)

    @router(api_parser)
    def evaluate_api(self):
       print("Evaluate API")

    @listen(evaluate_api)
    def generate_spring_boot_project(self):
        print("Generating Spring Boot Project")
        

    @listen(generate_spring_boot_project)
    def configure_application_properties(self):
        print("Configuring Application Properties")
    
    @router(configure_application_properties)
    def SpringBootApplication(self):
        print("Spring Boot Application")
      
       
            
      
    
   


def kickoff():
    poem_flow = CodeGenerator()
    poem_flow.kickoff()


def plot():
    poem_flow = CodeGenerator()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()

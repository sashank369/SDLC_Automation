import os
import subprocess

def build_and_run_springboot(project_directory):
    
    try:
        project_directory = os.path.abspath(project_directory)
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
            print("Build Output:", build_process.stdout.decode())
        
        # Run the built JAR file
        jar_file = "target/demo-0.0.1-SNAPSHOT.jar"  # Adjust according to your project
        run_command = ["java", "-jar", jar_file]
        subprocess.Popen(run_command,shell=True)

        print("Spring Boot application is running...")
    except subprocess.CalledProcessError as e:
        print(f"Error during build or execution: {e}")
    except FileNotFoundError as e:
        print(f"Directory not found: {project_directory}. Please check the path.")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Provide the full path to your Spring Boot project directory
project_directory = "demo"
build_and_run_springboot(project_directory)

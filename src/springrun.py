import os
import subprocess

def build_and_run_springboot(project_path):
    try:
        # Navigate to the Spring Boot project directory
        os.chdir(project_path)
        
        # Build the project
        build_command = ["mvn", "clean", "package"]
        subprocess.check_call(build_command)

        # Run the built JAR file
        jar_file = "target/demo-0.0.1-SNAPSHOT.jar"  # Adjust according to your project
        run_command = ["java", "-jar", jar_file]
        subprocess.Popen(run_command)

        print("Spring Boot application is running...")
    except subprocess.CalledProcessError as e:
        print(f"Error during build or execution: {e}")
    except FileNotFoundError as e:
        print(f"Directory not found: {project_path}. Please check the path.")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Provide the full path to your Spring Boot project directory
project_directory = "../demo"
build_and_run_springboot(project_directory)

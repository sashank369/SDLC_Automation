import os
import subprocess
import time

# Define paths
USER_REGISTRATION_MAIN = "C:/Users/Sashank Reddy/Desktop/EGov/SDLC_Automation/user_registration_crewai/main.py"
PRD_FILE_PATH = "C:/Users/Sashank Reddy/Desktop/EGov/SDLC_Automation/prd_document.md"
API_SPECS_MAIN = "C:/Users/Sashank Reddy/Desktop/EGov/SDLC_Automation/crewai_api_specs/backend_specs/main.py"
Backend_Path = "C:/Users/Sashank Reddy/Desktop/EGov/SDLC_Automation/src/djangogenerator/main.py"
def run_user_registration():
    print("\n📋 Running User Registration Crew...")
    subprocess.run(["python", USER_REGISTRATION_MAIN], check=True)
    wait_for_prd(PRD_FILE_PATH)

def wait_for_prd(file_path, timeout=60):
    print("\n🕒 Waiting for PRD document to be generated...")
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time > timeout:
            raise TimeoutError("❌ PRD document generation timed out!")
        time.sleep(2)
    print("✅ PRD document generated successfully!")

def run_api_specs():
    print("\n📄 Running API Specs Crew with PRD as input...")
    subprocess.run(["python", API_SPECS_MAIN, PRD_FILE_PATH], check=True)

def wait_for_swagger(file_path, timeout=60):
    print("\n⏳ Waiting for Swagger YAML to be generated...")
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time > timeout:
            raise TimeoutError("❌ Swagger YAML generation timed out!")
        time.sleep(2)
    print("✅ Swagger YAML file generated successfully!")

def generated_backend():
    wait_for_swagger(SWAGGER_YAML_PATH)
    subprocess.run(["python", Backend_Path], check=True)

if __name__ == "__main__":
    print("\n🚀 Starting the full automation process...\n")
    run_user_registration()
    run_api_specs()
    generated_backend()
    print("\n✅ Full process completed successfully!")

import os
import subprocess
import time

# Define paths
USER_REGISTRATION_MAIN = "C:/Users/Sashank Reddy/Desktop/EGov/SDLC_Automation/user_registration_crewai/main.py"
PRD_FILE_PATH = "C:/Users/Sashank Reddy/Desktop/EGov/SDLC_Automation/prd_document.md"
API_SPECS_MAIN = "C:/Users/Sashank Reddy/Desktop/EGov/SDLC_Automation/crewai_api_specs/backend_specs/main.py"
Backend_Path = "C:/Users/Sashank Reddy/Desktop/EGov/SDLC_Automation/src/djangogenerator/main.py"
def run_user_registration():
    print("\n Running User Registration Crew...")
    subprocess.run(["python", USER_REGISTRATION_MAIN], check=True)
    
    # Wait for PRD file to be generated
    wait_for_prd(PRD_FILE_PATH)

def wait_for_prd(file_path, timeout=60):
    """Waits until PRD file is created (max wait time = 60 sec)."""
    print("\n Waiting for PRD document to be generated...")
    start_time = time.time()
    while not os.path.exists(file_path):
        if time.time() - start_time > timeout:
            raise TimeoutError(" PRD document generation timed out!")
        time.sleep(2)  # Check every 2 seconds
    print("\n PRD document generated successfully!")

def run_api_specs():
    print("\n Running API Specs Crew with PRD as input...")
    subprocess.run(["python", API_SPECS_MAIN, PRD_FILE_PATH], check=True)

def generated_backend():

    subprocess.run(["python", Backend_Path], check=True)
    

if __name__ == "__main__":
    print("\n Starting the full automation process...\n")
    
    # Step 1: Generate PRD
    run_user_registration()
    
    # Step 2: Use PRD to generate API specs
    run_api_specs()

    generated_backend()

    print("\n Full process completed successfully!")

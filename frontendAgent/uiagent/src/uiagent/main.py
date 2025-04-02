#!/usr/bin/env python
from random import randint
from dotenv import load_dotenv
import os

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start

from uiagent.crews.PromptInterpreterAgent.PromptInterpreterAgent import PromptInterpreterAgent
from uiagent.crews.figmadesign.figmadesign import figmadesign
from uiagent.crews.Code.Code import Codegen
import subprocess

import json
FIGMA_FILE_KEY = "abcdefgh123456"

# Load environment variables from .env file
load_dotenv()

class PoemState(BaseModel):
    result: str = ""
    response: str = ""
    project_name: str = ""
    
    text: str = """SaaS Dashboard UI Design Specification
# ... existing code ...
"""

class PoemFlow(Flow[PoemState]):

    @start()
    def generate_poem(self):
        print("Extracting the content")
        self.state.project_name = input("Enter the project name: ")
        
        result = (
            PromptInterpreterAgent()
            .crew()
            .kickoff(inputs={"text": self.state.text})
        )

        print("Poem generated", result.raw)
        self.state.result = result.raw
            
    @listen(generate_poem)
    def figma(self):
        print("Creating Figma design") 
        self.state.response = figmadesign().crew().kickoff(inputs={"ui_json": self.state.result}).raw
        print("Saving figma design")
        with open("figma_design.txt", "w") as f:
            f.write(self.state.response)

    @listen(figma)
    def codegen(self):
        print("Starting React app generation")
        project_name = self.state.project_name
        project_dir = os.path.abspath(project_name)
        
        try:
            # Step 1: Create the React app using CLI
            print(f"Creating new React app: {project_name}...")
            result = subprocess.run(
                f"npx create-react-app {project_name} --template typescript",
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            print(f"Successfully created React app: {project_name}")
            print(result.stdout)

            # Get absolute path to project directory
            print(f"Project directory: {project_dir}")

            # Install additional dependencies
            print("Installing additional dependencies...")
            dependencies = [
                "tailwindcss",
                "postcss",
                "autoprefixer",
                "react-router-dom",
                "@heroicons/react",
                "classnames",
                "@typescript-eslint/parser",
                "@typescript-eslint/eslint-plugin",
                "prettier",
                "eslint-config-prettier"
            ]

            # Install dependencies in project directory
            subprocess.run(
                f"npm install {' '.join(dependencies)}",
                shell=True,
                check=True,
                cwd=project_dir
            )

            # Create tailwind.config.js content
            tailwind_config = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}"""
            
            # Write tailwind.config.js
            with open(os.path.join(project_dir, 'tailwind.config.js'), 'w') as f:
                f.write(tailwind_config)

            # Update src/index.css with Tailwind directives
            css_content = """@tailwind base;
@tailwind components;
@tailwind utilities;"""
            
            with open(os.path.join(project_dir, 'src', 'index.css'), 'w') as f:
                f.write(css_content)

            # Create .eslintrc.js
            eslint_config = """{
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ]
}"""
            with open(os.path.join(project_dir, '.eslintrc.json'), 'w') as f:
                f.write(eslint_config)

            # Create .prettierrc
            prettier_config = """{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}"""
            with open(os.path.join(project_dir, '.prettierrc'), 'w') as f:
                f.write(prettier_config)

            # Update package.json scripts
            package_json_path = os.path.join(project_dir, 'package.json')
            with open(package_json_path, 'r') as f:
                package_json = json.load(f)
            
            package_json['scripts'].update({
                "lint": "eslint src/**/*.{ts,tsx}",
                "lint:fix": "eslint src/**/*.{ts,tsx} --fix",
                "format": "prettier --write src/**/*.{ts,tsx}",
                "type-check": "tsc --noEmit"
            })
            
            with open(package_json_path, 'w') as f:
                json.dump(package_json, f, indent=2)

        except subprocess.CalledProcessError as e:
            print(f"Error creating React app: {e.stderr if e.stderr else str(e)}")
            raise
        except Exception as e:
            print(f"Unexpected error in React app generation: {str(e)}")
            raise

    @listen(codegen)      
    def update_react_app(self):
        print("Updating React app with UI specification")
        try:
            codegen = Codegen()
            project_dir = os.path.abspath(self.state.project_name)

            # Generate/update React components
            result = codegen.crew().kickoff(
                inputs={
                    "ui_json": self.state.response,
                    "project_name": self.state.project_name,
                    "project_dir": project_dir
                }
            )

            # Validate and fix any errors
            print("\nChecking for errors and attempting fixes...")
            validation_result = codegen.validate_and_fix(project_dir)
            
            if validation_result["success"]:
                print(f"\n✅ {validation_result['message']}")
            else:
                print(f"\n⚠️ {validation_result['message']}")
                print("\nRemaining errors:")
                for error in validation_result["remaining_errors"]:
                    print(f"- {error}")

            return result

        except Exception as e:
            print(f"Error updating React app: {str(e)}")
            raise

def kickoff():
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()

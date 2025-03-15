import requests
import json
import subprocess
import os
import time
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, FileWriterTool
from typing import List, Dict, Any
import re

@CrewBase
class Codegen:
    """CrewAI process for generating React applications"""

    def __init__(self):
        self.agents = []
        self.tasks = []
        super().__init__()

    def _run_command(self, command: str, cwd: str = None, check: bool = True) -> subprocess.CompletedProcess:
        """Run a command and return its output"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=check,
                capture_output=True,
                text=True,
                cwd=cwd
            )
            return result
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e.stderr}")
            raise

    def _parse_error_message(self, error_text: str) -> Dict[str, Any]:
        """Parse error messages to identify specific issues"""
        error_info = {
            "type": None,
            "message": error_text,
            "file": None,
            "line": None,
            "suggestion": None
        }

        # Tailwind CSS configuration error
        if "tailwindcss" in error_text and "PostCSS plugin" in error_text:
            error_info["type"] = "tailwind_config"
            error_info["suggestion"] = "Install @tailwindcss/postcss-8 and update PostCSS config"

        # TypeScript type error
        elif "TS" in error_text:
            error_info["type"] = "typescript"
            # Extract file and line information
            match = re.search(r'(.*?)\((\d+),(\d+)\)', error_text)
            if match:
                error_info["file"] = match.group(1)
                error_info["line"] = match.group(2)

        # ESLint error
        elif "error" in error_text.lower() and ("expected" in error_text.lower() or "missing" in error_text.lower()):
            error_info["type"] = "eslint"

        # Build error
        elif "Failed to compile" in error_text:
            error_info["type"] = "build"

        return error_info

    def _fix_tailwind_config(self, project_dir: str) -> bool:
        """Fix Tailwind CSS configuration issues"""
        try:
            # Install correct Tailwind CSS dependencies
            self._run_command(
                "npm uninstall tailwindcss postcss autoprefixer",
                cwd=project_dir,
                check=False
            )
            self._run_command(
                "npm install -D tailwindcss@latest postcss@latest autoprefixer@latest @tailwindcss/postcss-8",
                cwd=project_dir
            )

            # Create postcss.config.js
            postcss_config = """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}"""
            with open(os.path.join(project_dir, 'postcss.config.js'), 'w') as f:
                f.write(postcss_config)

            # Update tailwind.config.js
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
            with open(os.path.join(project_dir, 'tailwind.config.js'), 'w') as f:
                f.write(tailwind_config)

            # Update src/index.css
            css_content = """@tailwind base;
@tailwind components;
@tailwind utilities;"""
            with open(os.path.join(project_dir, 'src', 'index.css'), 'w') as f:
                f.write(css_content)

            return True
        except Exception as e:
            print(f"Error fixing Tailwind configuration: {str(e)}")
            return False

    def _check_build_errors(self, project_dir: str) -> List[Dict[str, Any]]:
        """Check for build errors in the React application"""
        errors = []
        try:
            # Run npm build to check for compilation errors
            build_result = self._run_command("npm run build", cwd=project_dir, check=False)
            if build_result.returncode != 0:
                error_info = self._parse_error_message(build_result.stderr)
                errors.append(error_info)

            # Run ESLint to check for linting errors
            lint_result = self._run_command("npx eslint src/**/*.{ts,tsx} --max-warnings 0", cwd=project_dir, check=False)
            if lint_result.returncode != 0:
                error_info = self._parse_error_message(lint_result.stderr)
                errors.append(error_info)

            # Run TypeScript compiler to check for type errors
            tsc_result = self._run_command("npx tsc --noEmit", cwd=project_dir, check=False)
            if tsc_result.returncode != 0:
                error_info = self._parse_error_message(tsc_result.stderr)
                errors.append(error_info)

            # Check if development server can start
            start_result = self._run_command("npm start", cwd=project_dir, check=False)
            if start_result.returncode != 0:
                error_info = self._parse_error_message(start_result.stderr)
                errors.append(error_info)

        except Exception as e:
            errors.append({
                "type": "unknown",
                "message": str(e),
                "suggestion": "Check system configuration and dependencies"
            })

        return errors

    def _fix_errors(self, project_dir: str, errors: List[Dict[str, Any]]) -> bool:
        """Attempt to fix detected errors"""
        try:
            fixed_all = True
            for error in errors:
                print(f"\nAttempting to fix {error['type']} error...")
                
                if error['type'] == 'tailwind_config':
                    if not self._fix_tailwind_config(project_dir):
                        fixed_all = False
                
                elif error['type'] == 'typescript':
                    # Run TypeScript fixes
                    self._run_command("npx tsc --noEmit", cwd=project_dir, check=False)
                    self._run_command("npm install --save-dev @types/react @types/react-dom", cwd=project_dir)
                
                elif error['type'] == 'eslint':
                    # Run ESLint fixes
                    self._run_command("npx eslint src/**/*.{ts,tsx} --fix", cwd=project_dir, check=False)
                    self._run_command("npx prettier --write src/**/*.{ts,tsx}", cwd=project_dir, check=False)
                
                elif error['type'] == 'build':
                    # Clear cache and reinstall dependencies
                    self._run_command("npm cache clean --force", cwd=project_dir)
                    self._run_command("rm -rf node_modules package-lock.json", cwd=project_dir)
                    self._run_command("npm install", cwd=project_dir)

            # Verify fixes
            remaining_errors = self._check_build_errors(project_dir)
            if remaining_errors:
                print("\nRemaining errors after fixes:")
                for error in remaining_errors:
                    print(f"- Type: {error['type']}")
                    print(f"  Message: {error['message']}")
                    if error['suggestion']:
                        print(f"  Suggestion: {error['suggestion']}")
                fixed_all = False

            return fixed_all
        except Exception as e:
            print(f"Error fixing issues: {str(e)}")
            return False

    @agent
    def ReactAppGenerator(self) -> Agent:
        """Agent responsible for generating React application code"""
        agent = Agent(
            name="ReactAppGenerator",
            role="React Application Generator",
            goal="Generate and validate a modern React application with TypeScript and Tailwind CSS",
            backstory="Expert React developer with deep knowledge of modern web development practices and debugging",
            tools=[FileWriterTool()],
            verbose=True
        )
        self.agents.append(agent)
        return agent

    @agent
    def ErrorFixerAgent(self) -> Agent:
        """Agent responsible for fixing React application errors"""
        agent = Agent(
            name="ErrorFixerAgent",
            role="React Error Fixer",
            goal="Identify and fix errors in React applications",
            backstory="Expert in debugging and fixing React applications with deep knowledge of TypeScript and common React patterns",
            tools=[FileWriterTool()],
            verbose=True
        )
        self.agents.append(agent)
        return agent

    @task
    def GenerateReactApp(self) -> Task:
        """Task for generating React application code"""
        task = Task(
            description="Generate a React application based on UI specifications",
            agent=self.ReactAppGenerator(),
            expected_output="A fully functional React application with TypeScript and Tailwind CSS",
            context="""
            Create a modern React application based on the provided UI specifications.
            The application should include:
            1. TypeScript for type safety
            2. Tailwind CSS for styling
            3. React Router for navigation
            4. Proper component structure
            5. State management using React hooks and context
            6. Form handling and validation
            7. Responsive design
            8. Error boundaries and loading states
            """
        )
        self.tasks.append(task)
        return task

    @task
    def FixReactErrors(self) -> Task:
        """Task for fixing React application errors"""
        task = Task(
            description="Identify and fix errors in the React application",
            agent=self.ErrorFixerAgent(),
            expected_output="A list of fixed errors and remaining issues",
            context="""
            1. Check for build errors
            2. Check for TypeScript errors
            3. Check for ESLint errors
            4. Attempt to fix detected issues
            5. Verify fixes and report results
            """
        )
        self.tasks.append(task)
        return task

    @crew
    def crew(self) -> Crew:
        """Creates the React app generation and error fixing Crew"""
        # Initialize agents and tasks if not already done
        if not self.agents:
            self.ReactAppGenerator()
            self.ErrorFixerAgent()
        if not self.tasks:
            self.GenerateReactApp()
            self.FixReactErrors()

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

    def validate_and_fix(self, project_dir: str) -> Dict[str, Any]:
        """Validate the React application and fix any errors"""
        print("\nValidating React application...")
        errors = self._check_build_errors(project_dir)
        
        if not errors:
            return {"success": True, "message": "No errors found"}

        print("\nFound errors:")
        for error in errors:
            print(f"- Type: {error['type']}")
            print(f"  Message: {error['message']}")
            if error['suggestion']:
                print(f"  Suggestion: {error['suggestion']}")

        print("\nAttempting to fix errors...")
        if self._fix_errors(project_dir, errors):
            return {"success": True, "message": "All errors fixed successfully"}
        else:
            remaining_errors = self._check_build_errors(project_dir)
            return {
                "success": False,
                "message": "Some errors could not be fixed automatically",
                "remaining_errors": remaining_errors
            }


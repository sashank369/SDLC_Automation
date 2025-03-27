from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool, FileWriterTool  # Importing tools
from typing import Optional


@CrewBase
class Code_fix():
    """Autonomous Code Fixing Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def code_fixer(self) -> Agent:
        return Agent(
            config=self.agents_config['code_fixer'],
            tools=[FileReadTool(), FileWriterTool()],  # Enabling file reading and writing capabilities
            verbose=True
        )

    @task
    def code_fix_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_fixer_task'],
            output_format="json",
            output_keys=["file_path", "content"],  # Ensures full content is included
            use_tools=True  # Ensures tools (FileReadTool & FileWriteTool) are used
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Code Fix Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,  # Ensures files are read before being modified
            verbose=True
        )

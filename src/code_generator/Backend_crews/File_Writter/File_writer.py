import subprocess
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool,FileWriterTool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
load_dotenv()

@CrewBase
class FileWriter:
    
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    provider = os.getenv("PROVIDER", "openai") 
    llm = ChatOpenAI(model=os.getenv("MODEL"),openai_api_key=os.getenv("OPENAI_API_KEY"), model_kwargs={"litellm_provider": provider})

    @agent
    def spring_boot_file_writer(self) -> Agent:
        if 'spring_boot_file_writer' not in self.agents_config:
            raise KeyError("Missing configuration for 'spring_boot_file_writer' in agents_config.")
        return Agent(
            config=self.agents_config['spring_boot_file_writer'],
            allow_delegation=True,
            verbose=True,
            llm=self.llm,
            tools=[FileWriterTool()],
            memory=True,
        )

    @task
    def write_spring_boot_application(self) -> Task:
        if 'write_spring_boot_application' not in self.tasks_config:
            raise KeyError("Missing configuration for 'write_spring_boot_application' in tasks_config.")
        return Task(
            config=self.tasks_config['write_spring_boot_application'],
            agent=self.spring_boot_file_writer()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

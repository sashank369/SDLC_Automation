import subprocess
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool,FileWriterTool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
load_dotenv()

@CrewBase
class ModelLayer:
    

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    provider = os.getenv("PROVIDER", "openai") 
    llm = ChatOpenAI(model=os.getenv("MODEL"),openai_api_key=os.getenv("OPENAI_API_KEY"), model_kwargs={"litellm_provider": provider})
    @agent
    def model_developer(self) -> Agent:
        if 'model_developer' not in self.agents_config:
            raise KeyError("Missing configuration for 'model_developer' in agents_config.")
        return Agent(
            config=self.agents_config['model_developer'],
            allow_delegation=True,
            verbose=True,
            llm=self.llm,
            tools=[FileWriterTool()],
            memory=True,
        )

    @task
    def generate_model_layer(self) -> Task:
        if 'generate_model_layer' not in self.tasks_config:
            raise KeyError("Missing configuration for 'generate_model_layer' in tasks_config.")
        return Task(
            config=self.tasks_config['generate_model_layer'],
            agent=self.model_developer()
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

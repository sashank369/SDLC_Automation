from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

load_dotenv()

@CrewBase
class ApiParser:
 
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    provider = os.getenv("PROVIDER", "openai") 
    llm = ChatOpenAI(model=os.getenv("MODEL"),openai_api_key=os.getenv("OPENAI_API_KEY"), model_kwargs={"litellm_provider": provider})
    @agent
    def tech_lead(self) -> Agent:
        if 'tech_lead' not in self.agents_config:
            raise KeyError("Missing configuration for 'tech_lead' in agents_config.")
        return Agent(
            config=self.agents_config['tech_lead'],
            # allow_delegation=True,
            verbose=True,
            llm=self.llm,
            tools=[FileReadTool(file_path=os.getenv('API_CONTRACT_PATH'))],
            memory=True,
            # max_iter=70
        )

    @task
    def parse_api_contract(self) -> Task:
        if 'parse_api_contract' not in self.tasks_config:
            raise KeyError("Missing configuration for 'parse_api_contract' in tasks_config.")
        return Task(
            config=self.tasks_config['parse_api_contract'],
            agent=self.tech_lead()
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

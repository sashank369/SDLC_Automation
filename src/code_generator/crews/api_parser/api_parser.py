from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool
from dotenv import load_dotenv
import os
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
load_dotenv()

@CrewBase
class ApiParser:
    

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = LLM(model=os.getenv("MODEL"),temperature=0.1)

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def tech_lead(self) -> Agent:
        if 'tech_lead' not in self.agents_config:
            raise KeyError("Missing configuration for 'tech_lead' in agents_config.")
        return Agent(
            config=self.agents_config['tech_lead'],
            allow_delegation=True,
            verbose=True,
            llm=self.llm,
            tools=[FileReadTool(file_path=os.getenv('API_CONTRACT_PATH'))],
            memory=False,
            max_iter=70
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
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
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

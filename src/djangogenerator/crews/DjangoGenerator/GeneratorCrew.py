from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool,FileWriterTool
from dotenv import load_dotenv
import boto3
import os
from langchain_openai import ChatOpenAI

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


load_dotenv()

@CrewBase
class GeneratorCrew:
   
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    provider = os.getenv("PROVIDER", "openai") 
    llm = ChatOpenAI(model=os.getenv("MODEL"),openai_api_key=os.getenv("OPENAI_API_KEY"), model_kwargs={"litellm_provider": provider}, temperature=1.2)

    @agent
    def django_developer(self) -> Agent:
        tool1=FileReadTool(file_path=os.getenv('API_CONTRACT_PATH'))
        tool2=FileReadTool(file_path='./test.py')
        tool3=FileWriterTool()
        return Agent(   
            config=self.agents_config["django_developer"],
            verbose=True,
            llm=self.llm,
            tools=[tool1,tool2,tool3],
            memory=True,
        )

    @task
    def generate_django_backend(self) -> Task:
        return Task(
            config=self.tasks_config["generate_django_backend"],
            agent=self.django_developer()
        )

    @crew
    def crew(self) -> Crew:
        
        return Crew(
            agents=self.agents,  
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )

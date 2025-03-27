from typing import Optional
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI


# Load environment variables from the .env file
load_dotenv()

class EvaluateApiParserverify(BaseModel):
    valid: bool
    feedback: Optional[str] = None


@CrewBase
class EvaluateApiParser:
    """Evaluate API Parser crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    provider = os.getenv("PROVIDER", "openai") 
    llm = ChatOpenAI(model=os.getenv("MODEL"),openai_api_key=os.getenv("OPENAI_API_KEY"), model_kwargs={"litellm_provider": provider})

    @agent
    def evaluate_api(self) -> Agent:
        """Create the API evaluation agent."""
        return Agent(
            config=self.agents_config['evaluate_api'],
            verbose=True,
            llm=self.llm,
            tools=[FileReadTool(file_path=os.getenv('API_CONTRACT_PATH'))],
            memory=True,
        )

    @task
    def evaluate_api_task(self) -> Task:
        """Define the evaluation task."""
        return Task(
            config=self.tasks_config['evaluate_api_task'],
            output_pydantic=EvaluateApiParserverify,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the EvaluateApiParser crew."""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

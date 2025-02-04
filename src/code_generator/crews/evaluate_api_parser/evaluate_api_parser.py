from typing import Optional
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool
from pydantic import BaseModel
from dotenv import load_dotenv
import os

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

    @agent
    def evalute_api(self) -> Agent:
        """Create the API evaluation agent."""
        return Agent(
            config=self.agents_config['evalute_api'],
            verbose=True,
            tools=[FileReadTool(file_path=os.getenv('API_CONTRACT_PATH'))],
            memory=False,
        )

    @task
    def evalute_api_task(self) -> Task:
        """Define the evaluation task."""
        return Task(
            config=self.tasks_config['evalute_api_task'],
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

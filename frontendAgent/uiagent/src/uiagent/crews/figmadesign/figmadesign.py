import requests
import json
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class figmadesign:
    """CrewAI process for generating Figma designs from JSON UI specifications"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def figmadesign(self) -> Agent:
        return Agent(config=self.agents_config["figmadesign"])
    

    @task
    def figmadesignTask(self) -> Task:
        return Task(config=self.tasks_config["figmadesignTask"])

    @crew
    def crew(self) -> Crew:
        """Creates the UI generation Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


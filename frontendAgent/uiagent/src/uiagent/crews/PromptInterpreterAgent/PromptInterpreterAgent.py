from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class PromptInterpreterAgent:
    """PromptInterpreterAgent"""

   
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def PromptInterpreterAgent(self) -> Agent:
        return Agent(
            config=self.agents_config["PromptInterpreterAgent"],
        )

    @task
    def PromptInterpreterAgentTask(self) -> Task:
        return Task(
            config=self.tasks_config["PromptInterpreterAgentTask"],
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

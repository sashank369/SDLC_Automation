#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from djangogenerator.crews.DjangoGenerator.GeneratorCrew import GeneratorCrew


class PoemState(BaseModel):
    sentence_count: int = 1
    poem: str = ""


class GeneratorFlow(Flow[PoemState]):

    @start()
    def generate_sentence_count(self):
        
        print("Generating Django application...")
        result = (
            GeneratorCrew()
            .crew()
            .kickoff()
        )

        print("Poem generated", result.raw)
        self.state.poem = result.raw



def kickoff():
    generator_flow = GeneratorFlow()
    generator_flow.kickoff()


def plot():
    generator_flow = GeneratorFlow()
    generator_flow.plot()


if __name__ == "__main__":
    kickoff()

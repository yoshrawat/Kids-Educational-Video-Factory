# domain/agents/story_agent.py
from domain.interfaces.llm_provider import LLMProvider
from domain.entities.scene import Scene


class StoryAgent:

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    async def run(self, topic: str) -> list[Scene]:
        prompt = f"""
        Create a short kids animal story for topic: {topic}.
        Split into 4 scenes with narration and image prompts.
        """

        response = await self.llm.generate(prompt)

        # simple parsing placeholder
        scenes = [
            Scene(
                description="Scene 1",
                image_prompt="cute rabbit forest cartoon",
                narration=response[:120],
            )
        ]

        return scenes
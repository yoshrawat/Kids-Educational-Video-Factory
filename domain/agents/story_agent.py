# domain/agents/story_agent.py
from domain.interfaces.llm_provider import LLMProvider
from domain.entities.scene import Scene
from shared.logging.logger import get_logger

from pathlib import Path
import uuid

logger = get_logger("story-agent")

STORY_DIR = Path("outputs/stories")
STORY_DIR.mkdir(parents=True, exist_ok=True)

class StoryAgent:

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    async def run(self, topic: str) -> list[Scene]:
        prompt = f"""
        Create a short kids animal story for topic: {topic}.
        Split into 4 scenes with narration and image prompts.
        """

        response = await self.llm.generate(prompt)

        logger.info("Story generated")

        # ⭐ Save story to file
        story_file = STORY_DIR / f"story_{uuid.uuid4()}.txt"
        story_file.write_text(response)

        logger.info(f"Story saved at: {story_file}")

        # simple parsing placeholder
        scenes = [
            Scene(
                description="Scene 1",
                image_prompt="cute rabbit forest cartoon",
                narration=response[:120],
            )
        ]

        return scenes
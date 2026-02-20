# domain/agents/metadata_agent.py
from domain.interfaces.llm_provider import LLMProvider


class MetadataAgent:

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    async def run(self, story_summary: str):
        prompt = f"""
        Generate:
        - engaging kids video title
        - SEO description for parents
        - 15 trending hashtags
        """

        return await self.llm.generate(prompt)
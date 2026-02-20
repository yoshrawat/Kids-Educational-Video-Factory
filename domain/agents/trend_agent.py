# domain/agents/trend_agent.py
from domain.interfaces.llm_provider import LLMProvider


class TrendAgent:

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    async def run(self, theme: str) -> str:
        prompt = f"""
        Find trending educational kids topics and hashtags for: {theme}.
        Age group 2-8.
        Return topic and hashtags.
        """
        return await self.llm.generate(prompt)
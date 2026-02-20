# app/orchestrators/langgraph_orchestrator.py
from langgraph.graph import StateGraph


class VideoOrchestrator:

    def __init__(self, pipeline):
        self.pipeline = pipeline

    async def run(self, theme: str):
        return await self.pipeline.run(theme)
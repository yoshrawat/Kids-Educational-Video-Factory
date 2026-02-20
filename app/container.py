# app/container.py
from infrastructure.config.provider_factory import get_llm
from domain.agents.trend_agent import TrendAgent
from domain.agents.story_agent import StoryAgent
from domain.agents.metadata_agent import MetadataAgent
from app.pipelines.video_pipeline import VideoPipeline


def build_pipeline():
    llm = get_llm()

    trend = TrendAgent(llm)
    story = StoryAgent(llm)
    meta = MetadataAgent(llm)

    return VideoPipeline(trend, story, meta)
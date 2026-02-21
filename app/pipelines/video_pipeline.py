# app/pipelines/video_pipeline.py
from domain.entities.video_project import VideoProject
from domain.agents.trend_agent import TrendAgent
from domain.agents.story_agent import StoryAgent
from domain.agents.metadata_agent import MetadataAgent

from workers.video_worker import generate_video_job
from workers.upload_worker import upload_video_job


class VideoPipeline:

    def __init__(
        self,
        trend_agent: TrendAgent,
        story_agent: StoryAgent,
        metadata_agent: MetadataAgent,
    ):
        self.trend_agent = trend_agent
        self.story_agent = story_agent
        self.metadata_agent = metadata_agent

    async def run(self, theme: str) -> VideoProject:
        project = VideoProject(theme=theme)

        # 1️⃣ Trend discovery
        trend_context = await self.trend_agent.run(theme)

        # 2️⃣ Story generation
        project.scenes = await self.story_agent.run(trend_context)

        # 3️⃣ Trigger async video generation
        # Convert dataclass to dict for JSON serialization
        from dataclasses import asdict
        # generate_video_job.send(asdict(project))
        generate_video_job.send(project.to_dict())

        return project
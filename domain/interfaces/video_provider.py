# domain/interfaces/video_provider.py
from abc import ABC, abstractmethod


class VideoProvider(ABC):

    @abstractmethod
    async def render(self, scenes: list[str], audio: str) -> str:
        pass
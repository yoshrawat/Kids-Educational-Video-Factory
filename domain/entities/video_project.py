# domain/entities/video_project.py
from dataclasses import dataclass, field
from typing import List
from .scene import Scene


@dataclass
class VideoProject:
    theme: str
    scenes: List[Scene] = field(default_factory=list)
    audio_path: str | None = None
    video_path: str | None = None
    subtitles_path: str | None = None
    title: str | None = None
    description: str | None = None
    hashtags: list[str] = field(default_factory=list)
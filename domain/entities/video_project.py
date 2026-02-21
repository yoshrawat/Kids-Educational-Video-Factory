from dataclasses import dataclass, field, asdict
from typing import List
from .scene import Scene


@dataclass
class VideoProject:
    theme: str
    scenes: List[Scene] = field(default_factory=list)
    audio_path: str | None = None
    video_path: str | None = None
    subtitles_path: str | None = None

    def to_dict(self):
        data = asdict(self)
        data["scenes"] = [s.to_dict() for s in self.scenes]
        return data

    @staticmethod
    def from_dict(data):
        # Create a copy to avoid in-place modification of the original dict
        # which causes serialization errors in Dramatiq retries
        data_copy = data.copy()
        if "scenes" in data_copy:
            data_copy["scenes"] = [Scene.from_dict(s) for s in data_copy["scenes"]]
        return VideoProject(**data_copy)
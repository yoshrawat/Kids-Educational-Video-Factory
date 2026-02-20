# domain/entities/scene.py
from dataclasses import dataclass


@dataclass
class Scene:
    description: str
    image_prompt: str
    narration: str
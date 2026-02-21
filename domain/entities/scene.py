from dataclasses import dataclass, asdict


@dataclass
class Scene:
    description: str
    image_prompt: str
    narration: str

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data):
        # Handle both dict and Scene objects
        if isinstance(data, Scene):
            return data
        return Scene(**data)
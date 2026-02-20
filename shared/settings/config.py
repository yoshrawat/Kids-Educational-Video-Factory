from pathlib import Path
import yaml
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parents[2]   # project root
CONFIG_PATH = BASE_DIR / "config.yaml"


class LLMConfig(BaseModel):
    provider: str
    model: str


class VideoConfig(BaseModel):
    resolution: str = "1080p"


class TTSConfig(BaseModel):
    provider: str
    languages: list[str]


class AppConfig(BaseModel):
    llm: LLMConfig
    video: VideoConfig
    tts: TTSConfig


def load_config() -> AppConfig:
    data = yaml.safe_load(CONFIG_PATH.read_text())
    return AppConfig(**data)


config = load_config()
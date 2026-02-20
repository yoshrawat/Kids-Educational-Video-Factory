# infrastructure/config/provider_factory.py
from infrastructure.llm.litellm_provider import LiteLLMProvider
from infrastructure.tts.coqui_tts_provider import CoquiTTSProvider
from infrastructure.video.moviepy_video_provider import MoviePyVideoProvider


def get_llm():
    return LiteLLMProvider()


def get_tts():
    return CoquiTTSProvider()


def get_video():
    return MoviePyVideoProvider()
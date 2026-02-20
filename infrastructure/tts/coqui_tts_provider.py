# infrastructure/tts/coqui_tts_provider.py
from TTS.api import TTS
from domain.interfaces.tts_provider import TTSProvider
from pathlib import Path
import uuid


class CoquiTTSProvider(TTSProvider):

    def __init__(self):
        self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

    async def synthesize(self, text: str, lang: str) -> str:
        path = f"outputs/audio_{uuid.uuid4()}.wav"
        self.tts.tts_to_file(text=text, file_path=path, language=lang)
        return path
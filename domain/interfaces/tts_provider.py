# domain/interfaces/tts_provider.py
from abc import ABC, abstractmethod


class TTSProvider(ABC):

    @abstractmethod
    async def synthesize(self, text: str, lang: str) -> str:
        pass
# infrastructure/tts/coqui_tts_provider.py

import os
os.environ['TTS_HOME'] = os.path.expanduser('~/.local/share/tts')
os.environ["COQUI_TOS_AGREED"] = "1"

# Monkey patch torch.load to allow loading old checkpoints
import torch
_original_torch_load = torch.load

def patched_torch_load(f, *args, **kwargs):
    # Set weights_only=False if not specified (for PyTorch 2.6+ compatibility)
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return _original_torch_load(f, *args, **kwargs)

torch.load = patched_torch_load

from TTS.api import TTS
from domain.interfaces.tts_provider import TTSProvider
from pathlib import Path
import uuid


class CoquiTTSProvider(TTSProvider):

    def __init__(self):
        self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

    async def synthesize(self, text: str, lang: str) -> str:
        # Create outputs directory if it doesn't exist
        os.makedirs('outputs', exist_ok=True)
        
        path = f"outputs/audio_{uuid.uuid4()}.wav"
        # Get available speakers from the speaker manager
        try:
            if hasattr(self.tts, 'synthesizer') and hasattr(self.tts.synthesizer, 'tts_model'):
                speakers = list(self.tts.synthesizer.tts_model.speaker_manager.speakers.keys())
                speaker = speakers[0] if speakers else None
            else:
                speaker = None
        except:
            speaker = None
        
        # Synthesize with or without speaker (speaker is optional for XTTS)
        if speaker:
            self.tts.tts_to_file(text=text, file_path=path, language=lang, speaker=speaker)
        else:
            self.tts.tts_to_file(text=text, file_path=path, language=lang)
        return path
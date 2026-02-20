# infrastructure/subtitle/whisper_subtitle.py
import whisper
import pysrt


class WhisperSubtitleService:

    def __init__(self):
        self.model = whisper.load_model("base")

    def generate(self, audio_path: str, out: str = "sub.srt"):
        result = self.model.transcribe(audio_path)

        subs = pysrt.SubRipFile()

        for i, seg in enumerate(result["segments"]):
            subs.append(
                pysrt.SubRipItem(
                    index=i,
                    start=self._fmt(seg["start"]),
                    end=self._fmt(seg["end"]),
                    text=seg["text"],
                )
            )

        subs.save(out)
        return out

    def _fmt(self, seconds: float):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"
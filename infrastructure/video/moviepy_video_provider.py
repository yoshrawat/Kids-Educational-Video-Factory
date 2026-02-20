# infrastructure/video/moviepy_video_provider.py
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    TextClip,
    concatenate_videoclips,
)
from domain.interfaces.video_provider import VideoProvider
from pathlib import Path
import uuid


class MoviePyVideoProvider(VideoProvider):

    async def render(self, scenes: list[str], audio: str) -> str:
        clips = []

        for img in scenes:
            clip = ImageClip(img).set_duration(5)

            # camera zoom motion
            clip = clip.resize(lambda t: 1 + 0.04 * t)

            # animated text bubble
            bubble = TextClip(
                "Learning is fun!",
                fontsize=50,
                color="yellow",
                bg_color="black",
            ).set_duration(3).set_position(("center", "top"))

            final = CompositeVideoClip([clip, bubble])
            clips.append(final)

        video = concatenate_videoclips(clips)

        video = video.set_audio(AudioFileClip(audio))

        out = f"outputs/video_{uuid.uuid4()}.mp4"
        video.write_videofile(out, fps=24)

        return out
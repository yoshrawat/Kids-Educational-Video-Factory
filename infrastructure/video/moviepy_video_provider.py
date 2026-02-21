# infrastructure/video/moviepy_video_provider.py
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
)
from infrastructure.video.comfyui_client import ComfyUIClient
from infrastructure.video.placeholder_image_generator import PlaceholderImageGenerator
from domain.interfaces.video_provider import VideoProvider
import uuid
import os


class MoviePyVideoProvider(VideoProvider):

    def __init__(self):
        self.comfy = ComfyUIClient()
        self.placeholder_generator = PlaceholderImageGenerator()
        os.makedirs('outputs', exist_ok=True)

    async def render(self, scenes, audio):
        clips = []

        for scene in scenes:
            enriched_prompt = (
                f"{scene.image_prompt}, dreamshaper style, "
                "storybook illustration, soft lighting, vibrant colors"
            )

            # Try ComfyUI first, fallback to placeholders on error
            try:
                images = [self.comfy.generate_image(enriched_prompt) for _ in range(3)]
            except Exception as e:
                print(f"ComfyUI image generation failed: {e}. Using placeholder images instead.")
                images = [self.placeholder_generator.generate(enriched_prompt) for _ in range(3)]

            for img in images:
                clip = ImageClip(img).set_duration(2.5)
                clips.append(clip)

        video = concatenate_videoclips(clips)
        video = video.set_audio(AudioFileClip(audio))

        out = f"outputs/video_{uuid.uuid4()}.mp4"
        video.write_videofile(out, fps=24, verbose=False, logger=None)

        return out
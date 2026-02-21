# infrastructure/video/moviepy_video_provider.py
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    TextClip,
    concatenate_videoclips,
)
from infrastructure.video.comfyui_client import ComfyUIClient
from infrastructure.video.placeholder_image_generator import PlaceholderImageGenerator
from domain.interfaces.video_provider import VideoProvider
import uuid
import os
from pathlib import Path


class MoviePyVideoProvider(VideoProvider):

    def __init__(self):
        self.comfy = ComfyUIClient()
        self.placeholder_generator = PlaceholderImageGenerator()

    async def render(self, scenes, audio):
        os.makedirs('outputs', exist_ok=True)
        clips = []

        for scene in scenes:
            enriched_prompt = (
                f"{scene.image_prompt}, dreamshaper style, "
                "storybook illustration, soft lighting, vibrant colors"
            )

            # Try to generate images with ComfyUI, fallback to placeholders
            images = []
            try:
                for _ in range(3):
                    img_path = self.comfy.generate_image(enriched_prompt)
                    # Verify file exists before adding
                    if Path(img_path).exists():
                        images.append(img_path)
                    else:
                        print(f"Warning: Generated image file not found at {img_path}")
                        # Fallback to placeholder
                        images.append(self.placeholder_generator.generate(enriched_prompt))
            except Exception as e:
                print(f"ComfyUI generation failed: {e}. Using placeholder images instead.")
                images = [self.placeholder_generator.generate(enriched_prompt) for _ in range(3)]

            for img in images:
                try:
                    clip = ImageClip(img).set_duration(2.5)

                    bubble = (
                        TextClip(
                            scene.narration[:45],
                            fontsize=40,
                            color="yellow",
                            bg_color="black",
                            font="/Users/yogeshrawat/Library/Fonts/Arial.TTF",
                        )
                        .set_duration(2.5)
                        .set_position(("center", "top"))
                    )

                    clips.append(CompositeVideoClip([clip, bubble]))
                except Exception as e:
                    print(f"Error creating clip for image {img}: {e}")
                    continue

        if not clips:
            raise RuntimeError("No video clips could be created")

        video = concatenate_videoclips(clips)
        video = video.set_audio(AudioFileClip(audio))

        out = f"outputs/video_{uuid.uuid4()}.mp4"
        video.write_videofile(out, fps=24, verbose=False, logger=None)

        return out
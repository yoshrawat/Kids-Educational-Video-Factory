# infrastructure/video/moviepy_video_provider.py
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
)
from domain.interfaces.video_provider import VideoProvider
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import uuid
import os


class MoviePyVideoProvider(VideoProvider):

    def __init__(self):
        os.makedirs('outputs', exist_ok=True)

    async def render(self, scenes: list[str], audio: str) -> str:
        clips = []

        for img in scenes:
            # Load the image and add text overlay
            pil_img = Image.open(img)
            draw = ImageDraw.Draw(pil_img)
            
            # Try to use a nice font, fallback to default
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
            except (OSError, IOError):
                font = ImageFont.load_default()
            
            # Add text overlay
            text = "Learning is fun!"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (pil_img.width - text_width) // 2
            y = 20
            draw.text((x, y), text, fill=(255, 255, 0), font=font)
            
            # Save the modified image temporarily
            temp_img_path = f"outputs/temp_scene_{uuid.uuid4()}.png"
            pil_img.save(temp_img_path)
            
            # Create clip from modified image
            clip = ImageClip(temp_img_path).set_duration(5)
            clips.append(clip)

        video = concatenate_videoclips(clips)
        video = video.set_audio(AudioFileClip(audio))

        out = f"outputs/video_{uuid.uuid4()}.mp4"
        video.write_videofile(out, fps=24, verbose=False, logger=None)

        return out
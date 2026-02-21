# infrastructure/video/pillow_text.py
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import uuid


class PillowTextRenderer:

    def __init__(self):
        self.font_path = self._get_font()

    def _get_font(self):
        # fallback system font
        return "/System/Library/Fonts/Supplemental/Arial.ttf"

    def render(self, text: str) -> str:
        img = Image.new("RGBA", (900, 200), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype(self.font_path, 48)

        draw.rectangle((0, 0, 900, 200), fill=(0, 0, 0, 180), outline=(255, 255, 0))
        draw.text((40, 70), text, font=font, fill=(255, 255, 0))

        out = f"outputs/bubble_{uuid.uuid4()}.png"
        img.save(out)

        return out
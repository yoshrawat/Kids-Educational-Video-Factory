"""Generate placeholder images from prompts for video scenes."""

import os
from PIL import Image, ImageDraw, ImageFont
import uuid


class PlaceholderImageGenerator:
    """Generate simple placeholder images with text from prompts."""
    
    def __init__(self, width: int = 1280, height: int = 720):
        self.width = width
        self.height = height
        os.makedirs('outputs', exist_ok=True)
    
    def generate(self, prompt: str) -> str:
        """
        Generate a placeholder image from a prompt.
        
        Args:
            prompt: Text description of the image
            
        Returns:
            Path to the generated image file
        """
        # Create a new image with a gradient-like background
        image = Image.new('RGB', (self.width, self.height), color=(70, 130, 180))
        draw = ImageDraw.Draw(image)
        
        # Try to use a nice font, fallback to default
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
            small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        except (OSError, IOError):
            font = ImageFont.load_default()
            small_font = font
        
        # Draw decorative shapes
        draw.rectangle([50, 50, self.width - 50, self.height - 50], outline=(255, 255, 255), width=5)
        draw.ellipse([100, 100, 300, 300], fill=(100, 200, 255), outline=(255, 255, 255), width=3)
        
        # Add prompt text - wrap it for readability
        max_chars_per_line = 30
        lines = []
        words = prompt.split()
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > max_chars_per_line:
                lines.append(' '.join(current_line[:-1]))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        # Center the text
        y_offset = self.height // 2 - len(lines) * 30
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (self.width - text_width) // 2
            draw.text((x, y_offset), line, fill=(255, 255, 255), font=font)
            y_offset += 60
        
        # Add a label
        draw.text((20, self.height - 60), "Generated Placeholder", fill=(200, 200, 200), font=small_font)
        
        # Save the image
        image_path = f"outputs/image_{uuid.uuid4()}.png"
        image.save(image_path)
        
        return image_path

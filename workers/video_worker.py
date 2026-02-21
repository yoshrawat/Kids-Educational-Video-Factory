# workers/video_worker.py
import dramatiq
import asyncio
from infrastructure.queue.redis_broker import broker

from infrastructure.config.provider_factory import (
    get_tts,
    get_video,
)

from infrastructure.subtitle.whisper_subtitle import WhisperSubtitleService
from infrastructure.video.placeholder_image_generator import PlaceholderImageGenerator
from workers.upload_worker import upload_video_job
from shared.logging.logger import get_logger
from domain.entities.video_project import VideoProject
from domain.entities.scene import Scene

logger = get_logger("video-worker")

# Lazy initialization - defer loading until first use
_tts = None
_video_provider = None
_subtitle_service = None

def get_tts_instance():
    global _tts
    if _tts is None:
        _tts = get_tts()
    return _tts

def get_video_provider_instance():
    global _video_provider
    if _video_provider is None:
        _video_provider = get_video()
    return _video_provider

def get_subtitle_service_instance():
    global _subtitle_service
    if _subtitle_service is None:
        _subtitle_service = WhisperSubtitleService()
    return _subtitle_service


@dramatiq.actor(max_retries=2)
def generate_video_job(project_dict):
    logger.info("Starting video generation")

    # Import here to avoid circular imports and ensure it's available on retries
    from dataclasses import asdict

    # Reconstruct VideoProject from dictionary
    if isinstance(project_dict, dict):
        # Reconstruct scenes as Scene objects
        scenes = [Scene(**s) if isinstance(s, dict) else s for s in project_dict.get('scenes', [])]
        project_dict['scenes'] = scenes
        project = VideoProject(**project_dict)
    else:
        project = project_dict

    # Get instances on first use
    tts = get_tts_instance()
    video_provider = get_video_provider_instance()
    subtitle_service = get_subtitle_service_instance()

    try:
        # 1️⃣ Merge narration
        narration_text = " ".join([s.narration for s in project.scenes])

        # Call async methods using asyncio.run()
        audio = asyncio.run(tts.synthesize(narration_text, "en"))

        # 1.5️⃣ Generate placeholder images from prompts
        image_generator = PlaceholderImageGenerator()
        scene_images = [image_generator.generate(s.image_prompt) for s in project.scenes]
        
        # 2️⃣ Render video
        video_path = asyncio.run(video_provider.render(scene_images, audio))

        # 3️⃣ Subtitle
        subtitle = subtitle_service.generate(audio)

        project.audio_path = audio
        project.video_path = video_path
        project.subtitles_path = subtitle
    except Exception as e:
        # Convert to dict for retry - this ensures JSON serializability
        logger.error(f"Error in video generation: {e}")
        project_dict = asdict(project)
        project_dict['scenes'] = [asdict(s) if hasattr(s, '__dataclass_fields__') else s 
                                  for s in project_dict.get('scenes', [])]
        raise

    # Convert back to dict for upload worker (convert Scene objects to dicts too)
    project_data = asdict(project)
    # Ensure scenes are dictionaries for JSON serialization (critical for Dramatiq retries)
    project_data['scenes'] = [
        asdict(s) if hasattr(s, '__dataclass_fields__') else s 
        for s in project_data.get('scenes', [])
    ]
    upload_video_job.send(project_data)
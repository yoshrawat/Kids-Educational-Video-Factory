# workers/video_worker.py
import dramatiq
from infrastructure.queue.redis_broker import broker

from infrastructure.config.provider_factory import (
    get_tts,
    get_video,
)

from infrastructure.subtitle.whisper_subtitle import WhisperSubtitleService
from workers.upload_worker import upload_video_job
from shared.logging.logger import get_logger

logger = get_logger("video-worker")

tts = get_tts()
video_provider = get_video()
subtitle_service = WhisperSubtitleService()


@dramatiq.actor(max_retries=2)
def generate_video_job(project):
    logger.info("Starting video generation")

    # 1️⃣ Merge narration
    narration_text = " ".join([s.narration for s in project.scenes])

    audio = dramatiq.run(tts.synthesize(narration_text, "en"))

    # 2️⃣ Render video
    scene_images = [s.image_prompt for s in project.scenes]  # placeholder
    video_path = dramatiq.run(video_provider.render(scene_images, audio))

    # 3️⃣ Subtitle
    subtitle = subtitle_service.generate(audio)

    project.audio_path = audio
    project.video_path = video_path
    project.subtitles_path = subtitle

    upload_video_job.send(project)
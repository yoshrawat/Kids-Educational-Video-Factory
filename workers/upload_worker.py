# workers/upload_worker.py
import dramatiq
from shared.logging.logger import get_logger

logger = get_logger("upload-worker")


@dramatiq.actor(max_retries=3)
def upload_video_job(project):
    logger.info(f"Uploading video: {project.video_path}")

    # TODO integrate YouTube / Instagram

    logger.info("Upload complete")
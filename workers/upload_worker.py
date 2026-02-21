# workers/upload_worker.py
import dramatiq
from shared.logging.logger import get_logger
from domain.entities.video_project import VideoProject

logger = get_logger("upload-worker")


@dramatiq.actor(max_retries=3)
def upload_video_job(project_dict):
    # Reconstruct VideoProject from dictionary if needed
    if isinstance(project_dict, dict):
        project = VideoProject(**project_dict)
    else:
        project = project_dict
    
    logger.info(f"Uploading video: {project.video_path}")

    # TODO integrate YouTube / Instagram

    logger.info("Upload complete")
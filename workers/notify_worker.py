# workers/notify_worker.py
import dramatiq
from shared.logging.logger import get_logger

logger = get_logger("notify-worker")


@dramatiq.actor
def notify_job(message: str):
    logger.info(f"Notification: {message}")
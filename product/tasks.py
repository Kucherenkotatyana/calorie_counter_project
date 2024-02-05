from celery import shared_task
from celery.utils.log import get_task_logger

from services.product_updater import ProductUpdater

logger = get_task_logger("celery_logger")


@shared_task()
def product_updater_scheduled_task():
    updater = ProductUpdater(batch_size=2)
    updater.update()

    logger.info("ProductUpdater executed")

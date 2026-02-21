import asyncio
import logging
from shared.repos.task_repo import TaskRepo
from shared.repos.ocr_repo import OCRRepo
from shared.db.database import SessionLocal
from shared.core.enums import TaskStatus
from shared.worker.ocr import OCR
from shared.utils.redis_client import get_redis_client, RedisClient
from shared.schemas.task_payload import TaskPayload
from shared.db.models import OCRTask
from shared.schemas.ocr_task_schema import OCRTaskSchema
from typing import Sequence
from shared.db.models import Image
from shared.schemas.image_schema import ImageSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Worker:
    def __init__(self, ocr: OCR, redis_client: RedisClient):
        self.redis_client = redis_client
        self.ocr = ocr

    async def process_task(self, payload: TaskPayload):
        task_id = payload.task_id

        async with SessionLocal() as session:
            task_repo = TaskRepo(session)
            ocr_repo = OCRRepo(session)

            try:
                task: OCRTask | None = await task_repo.get_task(task_id)
                if not task:
                    return
                task_schema: OCRTaskSchema = OCRTaskSchema.model_validate(task)
                if task_schema.status == TaskStatus.COMPLETED:
                    return

                await task_repo.update_task_status(task_id, TaskStatus.IN_PROGRESS)
                images: Sequence[Image] = await ocr_repo.get_images_by_task_id(task_id)

                for image in images:
                    image_schema: ImageSchema = ImageSchema.model_validate(image)
                    text: str = await asyncio.to_thread(
                        self.ocr.ocr_from_bytes, image_schema.image_bytes
                    )

                    await ocr_repo.update_image_text(image_schema.id, text)
                    logger.info(
                        f"Successfully processed image {image_schema.id}, task: {task_id}"
                    )

                await task_repo.update_task_status(task_id, TaskStatus.COMPLETED)
                logger.info(f"Successfully processed task {task_id}")

            except Exception as e:
                logger.error(f"Error processing task {task_id}: {e}")
                await task_repo.update_task_status(task_id, TaskStatus.FAILED)

                # Retry
                if payload.attempt < self.redis_client.MAX_ATTEMPTS:
                    logger.info(f"Retrying task {task_id}, attempt {payload.attempt}")
                    await self.redis_client.push_retry(payload)
                else:
                    logger.error(
                        f"Task {task_id} failed after max retries. Moving to dead letter."
                    )
                    await self.redis_client.push_dead(payload)


async def main():
    redis_client = get_redis_client()
    worker = Worker(ocr=OCR(), redis_client=redis_client)

    logger.info("Worker started and listening for tasks...")

    while True:
        try:
            task_payload: TaskPayload | None = await redis_client.pop_task(timeout=10)
            if task_payload:
                await worker.process_task(task_payload)
            await redis_client.promote_retries()

        except Exception as e:
            logger.error(f"Worker Loop Error: {e}")
            await asyncio.sleep(5)  # Cooldown on failure


if __name__ == "__main__":
    asyncio.run(main())

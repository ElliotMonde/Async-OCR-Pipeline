from shared.db.database import get_db
from shared.repos.ocr_repo import OCRRepo
from shared.repos.task_repo import TaskRepo
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from shared.db.models import OCRTask, Image
from shared.core.exceptions import NotFoundException, InternalServerErrorException
from shared.core.enums import TaskStatus
import base64
from typing import List, Sequence
from uuid import uuid4
from shared.schemas.image_schema import ImageSchema
from shared.schemas.task_payload import TaskPayload
from shared.schemas.ocr_task_schema import OCRTaskSchema
from shared.utils.redis_client import get_redis_client, RedisClient
from shared.worker.ocr import OCR


class OCRService:
    def __init__(
        self,
        ocr: OCR = Depends(),
        db_session: AsyncSession = Depends(get_db),
        redis_client: RedisClient = Depends(get_redis_client),
    ):
        self.ocr_repo = OCRRepo(db_session)
        self.task_repo = TaskRepo(db_session)
        self.redis_client = redis_client
        self.ocr = ocr

    async def get_task(self, task_id: str) -> List[str] | str | None:
        """
        Get OCR task result from database.

        Args:
            task_id (str): task id
        Returns:
            List[str] | None: list of image texts or None
        """
        task: OCRTask | None = await self.task_repo.get_task(task_id)
        if not task:
            raise NotFoundException(detail="Task not found")
        
        task_schema: OCRTaskSchema = OCRTaskSchema.model_validate(task)
        if task_schema.status in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS]:
            return [""] if task_schema.batch else ""

        if task_schema.status == TaskStatus.FAILED:
            raise InternalServerErrorException(detail="Task failed")
        print(f"status: {task.status}, batch: {task.batch}, task images: {task.images}")
        if task_schema.batch:
            return [image.text or "" for image in task.images]
        else:
            return task.images[0].text or "" if task.images else ""

    async def queue_task(self, image_data: str | List[str]) -> str:
        """
        Asynchronously queue OCR tasks into redis.

        Args:
            image_data (str): base64 encoded image string
        Returns:
            str: task id
        """
        # generate task id
        task_id: str = str(uuid4())
        is_batch = isinstance(image_data, List)

        task: OCRTask = OCRTask(
            task_id=task_id, status=TaskStatus.PENDING, batch=is_batch
        )
        if not await self.task_repo.create_task(task):
            raise InternalServerErrorException(detail="Failed to create task")

        if is_batch:
            image_binaries: List[bytes] = [
                base64.b64decode(image) for image in image_data
            ]
            await self.ocr_repo.add_image_binaries(task_id, image_binaries)
        else:
            image_binary: bytes = base64.b64decode(image_data)
            await self.ocr_repo.add_image_binary(task_id, image_binary)
        await self.redis_client.queue_task(TaskPayload(task_id=task_id))
        return task_id

    def sync_upload_image(self, image_data: str | List[str]) -> str | List[str]:
        """
        Synchronously upload image as base64 string and return OCR text

        Args:
            image_data (str): base64 encoded image string

        Returns:
            str: OCR result
        """
        try:
            if isinstance(image_data, List):
                return [self.ocr.ocr_from_b64(image) for image in image_data]
            return self.ocr.ocr_from_b64(image_data)
        except Exception as e:
            raise InternalServerErrorException(detail=str(e))

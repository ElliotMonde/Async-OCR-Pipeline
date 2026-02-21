from sqlalchemy import select, update
from shared.db.models import Image
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, List
from shared.core.exceptions import NotFoundException, InternalServerErrorException


class OCRRepo:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_image_by_id(self, image_id: int) -> Image:
        image: Image = await self.db_session.get(Image, image_id)
        if image is None:
            raise NotFoundException(detail="Image not found")
        return image

    async def get_images_by_task_id(self, task_id: str) -> Sequence[Image]:
        stmt = select(Image).where(Image.task_id == task_id)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get_image_by_task_id(self, task_id: str) -> Image:
        stmt = select(Image).where(Image.task_id == task_id)
        result = await self.db_session.execute(stmt)
        return result.scalars().first()

    async def add_image_binary(self, task_id: str, image_binary: bytes) -> bool:
        image = Image(task_id=task_id, image_bytes=image_binary)
        try:
            self.db_session.add(image)
            await self.db_session.commit()
        except Exception as e:
            raise InternalServerErrorException(detail=f"Failed to upload image")
        return True

    async def add_image_binaries(
        self, task_id: str, image_binaries: List[bytes]
    ) -> bool:
        try:
            for image_binary in image_binaries:
                if not await self.add_image_binary(task_id, image_binary):
                    return False
            return True
        except Exception as e:
            raise InternalServerErrorException(detail=f"Failed to upload images")

    async def update_image_text(self, image_id: int, text: str) -> bool:
        image: Image = await self.get_image_by_id(image_id)
        stmt = update(Image).where(Image.id == image.id).values(text=text)
        await self.db_session.execute(stmt)
        await self.db_session.commit()
        return True

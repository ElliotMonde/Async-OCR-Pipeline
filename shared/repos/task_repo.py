from sqlalchemy.ext.asyncio import AsyncSession
from shared.db.models import OCRTask
from sqlalchemy import update, select
from sqlalchemy.orm import selectinload
from shared.core.enums import TaskStatus


class TaskRepo:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_task(self, task_id: str) -> OCRTask | None:
        stmt = (
            select(OCRTask)
            .where(OCRTask.task_id == task_id)
            .options(selectinload(OCRTask.images))
        )
        result = await self.db_session.execute(stmt)
        return result.scalars().first()

    async def create_task(self, task: OCRTask) -> bool:
        self.db_session.add(task)
        await self.db_session.commit()
        return True

    async def update_task_status(self, task_id: str, status: TaskStatus) -> bool:
        stmt = update(OCRTask).where(OCRTask.task_id == task_id).values(status=status)
        await self.db_session.execute(stmt)
        await self.db_session.commit()
        return True

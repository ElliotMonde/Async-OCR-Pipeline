from datetime import datetime
from pydantic import BaseModel, ConfigDict
from shared.core.enums import TaskStatus
from typing import List
from shared.schemas.image_schema import ImageSchema

class OCRTaskSchema(BaseModel):
    id: int
    task_id: str
    status: TaskStatus
    batch: bool
    created_at: datetime
    updated_at: datetime
    images: List[ImageSchema]

    model_config = ConfigDict(from_attributes=True)

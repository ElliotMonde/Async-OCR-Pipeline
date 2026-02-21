from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ImageSchema(BaseModel):
    id: int
    task_id: str
    image_bytes: bytes
    text: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
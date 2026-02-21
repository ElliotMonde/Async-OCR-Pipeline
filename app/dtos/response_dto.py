from pydantic import BaseModel
from typing import List

class GetImageResponseDto(BaseModel):
    # task_id: "<recognized text>" or ["<recognized text>"] for batch
    task_id: str | List[str] | None


class PostImageResponseDto(BaseModel):
    # task_id: "<task id>"
    task_id: str

class SyncImageResponseDto(BaseModel):
    # text: "<recognized text> or [<recognized text>, ..] for batch"
    text: str | List[str]
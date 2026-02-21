import time
from pydantic import BaseModel

class TaskPayload(BaseModel):
    task_id: str
    attempt: int = 0
    max_attempts: int = 5
    created_at: int = int(time.time()) # unix seconds
    last_error: str | None = None
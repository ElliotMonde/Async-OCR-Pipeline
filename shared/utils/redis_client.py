import json
from time import time
from redis import asyncio as aioredis  # Use the asyncio version
from shared.core.config import settings
from shared.schemas.task_payload import TaskPayload
from shared.core.exceptions import InternalServerErrorException

class RedisClient:
    def __init__(self):
        # Initialize async connection
        self.client = aioredis.Redis(
            host=settings.REDIS_HOST,
            port=int(settings.REDIS_PORT),
            decode_responses=True,
            db=0,
        )
        self.QUEUE_KEY = "ocr:queue"
        self.RETRY_KEY = "ocr:retry"
        self.DEAD_KEY = "ocr:dead"
        self.MAX_ATTEMPTS = 3
        self.MAX_BACKOFF = 60

    async def queue_task(self, task_payload: TaskPayload) -> None:
        try:
            task_payload.attempt += 1
            await self.client.lpush(self.QUEUE_KEY, task_payload.model_dump_json())
            return
        except Exception:
            raise InternalServerErrorException(detail="Failed to queue task")



    async def pop_task(self, timeout=5) -> TaskPayload | None:
        try:
            result = await self.client.brpop([self.QUEUE_KEY], timeout=timeout)
            if result:
                _, payload = result
                return TaskPayload.model_validate(json.loads(payload))
            return None
        except Exception as e:
            print(f"Pop error: {e}")
            return None

    async def push_retry(self, payload: TaskPayload) -> None:
        score = int(time()) + self.compute_backoff(payload.attempt)
        await self.client.zadd(self.RETRY_KEY, {payload.model_dump_json(): score})

    async def push_dead(self, payload: TaskPayload) -> None:
        await self.client.lpush(self.DEAD_KEY, payload.model_dump_json())

    async def promote_retries(self):
        now = int(time())
        ready = await self.client.zrangebyscore(self.RETRY_KEY, 0, now)
        for payload_json in ready:
            await self.client.zrem(self.RETRY_KEY, payload_json)
            await self.client.lpush(self.QUEUE_KEY, payload_json)

    def compute_backoff(self, attempt: int) -> int:
        return min(2**attempt, self.MAX_BACKOFF)

_redis_instance = None

def get_redis_client() -> RedisClient:
    global _redis_instance
    if _redis_instance is None:
        _redis_instance = RedisClient()
    return _redis_instance

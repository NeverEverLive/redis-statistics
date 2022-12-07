import redis
from typing import Optional

from pydantic import BaseModel
from src.components.response.schema import BaseResponse


class RedisStats(BaseModel):
    health: Optional[int]
    resolution: Optional[str]


import logging

from fastapi import APIRouter


from src.components.response.schema import BaseResponse
from src.models.redis.base import get_session

router = APIRouter(prefix="/analitics")


@router.get("", response_model=BaseResponse, status_code=200)
def check_redis():
    try:
        session = get_session()
        session.set("foo", "bar")
        logging.warning(session.get("foo"))
        return {
            "message": "Redis is working"
        }
    except Exception as error:
        return {
            "message": f"Some problem with Redis + {str(error)}"
        }


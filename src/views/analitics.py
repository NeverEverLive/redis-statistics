import logging

from fastapi import APIRouter

from src.components.response.schema import BaseResponse
from src.models.redis.base import get_session
from src.components.analitic.schema import RedisStats

router = APIRouter(prefix="/analitics")


@router.get("", response_model=BaseResponse, status_code=200)
def check_redis():
    try:
        session = get_session()
        session.set("foo", "bar")
        for key in session.scan_iter():
            logging.warning(key)
            logging.warning(session.get(key))
        return {
            "message": "Redis is working"
        }
    except Exception as error:
        return {
            "message": f"Some problem with Redis + {str(error)}"
        }


@router.post("", response_model=BaseResponse, status_code=200)
def collect_data(stats: RedisStats):
    logging.warning(stats.dict())
    for key, value in stats.dict().items():
        logging.warning(key)
        logging.warning(value)
        if value:
            session = get_session()
            if stat := session.get(value):
                session.set(value, int(stat.decode()) + 1)
            else:
                session.set(value, 1)
    return {
        "message": "Analitics is collected",
    }


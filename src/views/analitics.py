import logging
import asyncio

from fastapi import APIRouter

from src.components.response.schema import BaseResponse
from src.models.redis.base import get_session
from src.components.analitic.schema import RedisStats

router = APIRouter(prefix="/analitics")


@router.get("", response_model=BaseResponse, status_code=200)
async def check_redis():
    try:
        session = await get_session()
        await session.set("foo", "bar")
        await session.set("asd", "qwe")
        logging.warning(await session.scan())
        keys = list(map(lambda x: x.decode("utf-8"), (await session.scan())[1]))
        tasks = [asyncio.create_task(session.get(key)) for key in keys]
        results = list(map(lambda x: x.decode(), await asyncio.gather(*tasks)))
        
        for index in range(len(results)):
            logging.warning(keys[index])
            logging.warning(results[index])

        return {
            "message": "Redis is working"
        }
    except Exception as error:
        return {
            "message": f"Some problem with Redis + {str(error)}"
        }


@router.post("", response_model=BaseResponse, status_code=200)
async def collect_data(stats: RedisStats):
    keys = []
    options = []

    for value in stats.dict().values():
        if value:
            session = await get_session()
            options.append(asyncio.create_task(session.get(value)))
            keys.append(value)

    tasks = []
    
    for index, stat in enumerate(list(map(lambda x: int(x.decode()), await asyncio.gather(*options)))):
        if stat:
            tasks.append(asyncio.create_task(session.set(keys[index], stat + 1)))
        else:
            tasks.append(asyncio.create_task(session.set(keys[index], 1)))
    
    return {
        "message": "Analitics is collected",
    }


from fastapi import APIRouter

from src.components.response.schema import BaseResponse


router = APIRouter()


@router.get("", response_model=BaseResponse, status_code=200)
async def health_check():
    try:
        return {
            "message": "It's alright"
        }
    except Exception as error:
        return {
            "message": str(error)
        }


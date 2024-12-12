from fastapi import APIRouter, status, Query, Depends, Path, Request, UploadFile, File
import uuid
from src.services import therapy_service
from src.utils.request_response import ApiResponse
from src.utils.app_notification_message import NotificationMessage
from typing import Dict, Union, List, Annotated

therapy_router = APIRouter(prefix="/therapy", tags=["Therapy"])

@therapy_router.post(
        '/analysis/',
        response_model=Dict[str, str],
        status_code=status.HTTP_201_CREATED
    )
async def send_session(
    user_id: str = Query(..., description="The ID of the user"),
    sessions: List[UploadFile] = File(...)
    ):
    result = await therapy_service.TherapyService.track_progress(user_id, sessions)
    return ApiResponse(
        message=NotificationMessage.PROGRESS_TRACKED,
        data=result
    )
from fastapi import UploadFile
import uuid
import json
from typing import Union, Dict, Optional, List
from mentalyc_ai import MentalycNoteAgent
from src.exceptions.custom_exception import (
    APIAuthenticationFailException, InternalServerException, RecordNotFoundException
)

from config.logger import Logger

logger = Logger(__name__)

class TherapyService:
    @staticmethod
    async def track_progress(user_id: Union[str, uuid.UUID], files: List[UploadFile]):
        try:
            note_agent = MentalycNoteAgent(user_id=user_id)
            sessions = {}
            for file in files:
                file_bytes = await file.read()
                session_content = json.loads(file_bytes.decode('utf-8'))
                session_id = file.filename.split('.')[0].split('_')[-1]
                sessions[session_id] = session_content

            result = note_agent(sessions)
            logger.info("Sessions processed successfully")
        except Exception as ex:
            logger.error(f"Processing Sessions -> API v1/therapy/analysis/: {ex}")
            raise InternalServerException()

        return result
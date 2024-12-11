import os
import uuid
from typing import List, Dict, Any

from fastapi import Request
from fastapi.responses import FileResponse
import pathlib
import json

from src.exceptions.custom_exception import AppException
from config.logger import Logger
from src.exceptions.custom_exception import RecordNotFoundException
from src.utils.app_notification_message import NotificationMessage

logger = Logger(__name__)


class AppUtil:
    @staticmethod
    def serialize_dict(a) -> dict:
        return {**{i: str(a[i]) for i in a if i == '_id'}, **{i: a[i] for i in a if i != '_id'}}

    @staticmethod
    def serialize_list(entity) -> list:
        return [AppUtil.serialize_dict(a) for a in entity]
    
    @staticmethod
    def load_file(path: pathlib.Path):
        with open(path, "r") as f:
            return f.read()
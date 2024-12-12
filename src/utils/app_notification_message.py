from pydantic import BaseModel


class NotificationMessage:
    PROGRESS_TRACKED = "Progress tracked successfully"
    INTERNAL_SERVER_ERROR = "Could not complete the request at the moment"
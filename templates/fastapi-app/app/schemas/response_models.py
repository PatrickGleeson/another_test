from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class StatusEnum(str, Enum):
    STATUS_UP = "healthy"
    STATUS_DOWN = "unhealthy"


class StatusMessage(BaseModel):
    status: StatusEnum
    error: Optional[str]


class Health(BaseModel):
    service: StatusMessage
    database: StatusMessage

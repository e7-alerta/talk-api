from typing import Optional
from pydantic import BaseModel, Field


class EventPayload(BaseModel):
    type: Optional[str] = Field(..., alias="type")
    text: Optional[str] = Field(..., alias="text")


class EventRequest(BaseModel):
    event_id: Optional[str] = Field(..., alias="eventId")
    event_name: Optional[str] = Field(..., alias="eventName")
    event_type: Optional[str] = Field(..., alias="eventType")
    text: Optional[str] = Field(..., alias="text")
    payload: Optional[EventPayload] = Field(..., alias="payload")

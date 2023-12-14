from typing import Optional

from pydantic import BaseModel


class ChatContact(BaseModel):
    id: Optional[str] = None
    name: str
    phone_number: str
    last_conversation_id: Optional[str] = None
    place_id: Optional[str] = None

from typing import Optional
from pydantic import BaseModel

from dash.types import DashContact, DashPlaceInfo


class CreateContactForm(BaseModel):
    dash_id: str
    phone: str
    name: str
    contact_type: Optional[str] = None
    place_id: Optional[str] = None
    chatwoot_id: Optional[str] = None
    keep_current_conversation: Optional[bool] = False


class SendPanicAlertForm(BaseModel):
    contact: DashContact
    place: DashPlaceInfo

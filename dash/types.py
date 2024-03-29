from typing import Optional

from pydantic import BaseModel


class DashException(Exception):
    """Base class for all Dash-related exceptions."""
    pass


class DashAuthenticationException(DashException):
    """Raised when authentication fails."""
    pass


class DashConnectionException(DashException):
    """Raised when a connection to the Dash server cannot be established."""
    pass


class DashRequestException(DashException):
    """Raised when a request to the Dash server fails."""
    pass


class DashParams(BaseModel):
    base_url: str


class DashPlaceInfo(BaseModel):
    id: str
    name: str
    address: Optional[str] = None
    street: Optional[str] = None
    street_number: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_owner: Optional[str] = None
    pass


class DashContact(BaseModel):
    id: str
    name: str
    phone: str
    contact_type: str
    place_id: Optional[str] = None
    chatwoot_id: Optional[str] = None
    last_conversation_id: Optional[str] = None
    pass


class DashPhoneInfo(BaseModel):
    id: Optional[str] = None
    phone_number: Optional[str] = None
    place: Optional[dict] = None
    contact: Optional[dict] = None
    pass

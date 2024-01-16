from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ContentType(Enum):
    TEXT = "text"
    IMAGE = "image"
    pass

    @classmethod
    def of(cls, value: str):
        if value == "text":
            return ContentType.TEXT
        elif value == "image":
            return ContentType.IMAGE
        raise Exception(f"Content type {value} not supported")


class SenderType(Enum):
    CONTACT = "contact"
    pass

    @classmethod
    def of(cls, value: str):
        if value == "contact":
            return SenderType.CONTACT
        raise Exception(f"Sender type {value} not supported")


class Sender(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    type: Optional[str] = None


class ConversationMeta(BaseModel):
    sender: Optional[Sender] = None


class Conversation(BaseModel):
    id: Optional[str] = None
    meta: Optional[ConversationMeta] = None


class MessageType(Enum):
    OUTGOING = "outgoing"
    INCOMING = "incoming"
    pass

    @classmethod
    def of(cls, param):
        if param == "outgoing":
            return MessageType.OUTGOING
        elif param == "incoming":
            return MessageType.INCOMING
        pass


class EventType(Enum):
    CONTACT_CREATED = "contact_created"
    CONVERSATION_CREATED = "conversation_created"
    MESSAGE_CREATED = "message_created"
    pass


class EventRequest(BaseModel):
    content_type: Optional[ContentType] = None
    content: Optional[str] = None
    conversation: Optional[Conversation] = None
    message_type: Optional[MessageType] = None
    sender: Optional[Sender] = None
    pass

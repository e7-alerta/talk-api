from enum import Enum
from typing import Optional

from pydantic import BaseModel, constr


class MessageType(Enum):
    INCOMMING = "incoming"
    OUTGOING = "outgoing"


class MessageIntent(Enum):
    CONTACT_GREETING = "contact_greeting"
    VECINO_GREETING = "vecino_greeting"
    PLACE_GREETING = "place_greeting"
    UNKNOWN = "unknown"


class MessageCreatedForm(BaseModel):
    content: constr(strip_whitespace=True)
    phone_number: constr(strip_whitespace=True)
    message_type: MessageType = None
    message_intent: Optional[MessageIntent] = None
    phone_key: Optional[str] = None
    sender_name: Optional[str] = None

    def __init__(self, content, phone_number, message_type):
        super().__init__(content=content, phone_number=phone_number, message_type=message_type)
        self._hydrate_form()

    def _hydrate_form(self):
        self.evaluate_message_intent()

        self.extract_phone_key()

    def evaluate_message_intent(self):
        if "🚨️🚨" in self.content:
            # self.message_type = "contact_greeting"
            self.message_intent = MessageIntent.VECINO_GREETING
        elif " 🚨 " in self.content:
            # self.message_type = "place_greeting"
            self.message_intent = MessageIntent.PLACE_GREETING
        else:
            self.message_intent = MessageIntent.UNKNOWN

    def is_vecino_greeting(self):
        return self.message_intent == MessageIntent.VECINO_GREETING

    def is_place_greeting(self):
        return self.message_intent == MessageIntent.PLACE_GREETING

    def extract_phone_key(self):
        keyword = "🚨️🚨" if self.message_intent == MessageIntent.CONTACT_GREETING else " 🚨 "
        index = self.content.find(keyword)
        if index != -1:
            self.phone_key = self.content[index + len(keyword): index + len(keyword) + 4]

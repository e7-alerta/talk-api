import json
from enum import Enum
from typing import Optional

from pydantic import BaseModel
from features.greeting.types import MessageCreatedForm


def _is_valid_event(webhook_data):
    return webhook_data.get("event") == "message_created"


def _get_event_type(webhook_data):
    return webhook_data.get("event")


def parse_message_created_event(data):
    try:
        # webhook_data = json.loads(data)
        if _is_valid_event(data):
            content = data.get("content", "")
            phone_number = data.get("conversation", {}).get("meta", {}).get("sender", {}).get("phone_number", "")
            message_type = data.get("message_type", "")

            form = MessageCreatedForm(content, phone_number, message_type)
            # extract a sender name from content
            sender_name = data.get("conversation", {}).get("meta", {}).get("sender", {}).get("name", "")
            # check si es vacio y si tiene numeros
            if sender_name == "" or any(char.isdigit() for char in sender_name):
                sender_name = data.get("sender", {}).get("name", "")
            if sender_name == "" or any(char.isdigit() for char in sender_name):
                sender_name = None
            form.sender_name = sender_name

            form.evaluate_message_intent()
            form.extract_phone_key()
            return form
    except json.JSONDecodeError as e:
        print("Error al analizar el JSON:", e)
    except Exception as e:
        print("Error:", e)


def parse_event(data):
    try:
        # webhook_data = json.loads(json_data)
        event_type = _get_event_type(data)
        event_payload = EventPayload(event=event_type, payload=data)
        if event_payload.is_message_created():
            event_payload.message_created_form = parse_message_created_event(data)
        return event_payload
    except json.JSONDecodeError as e:
        print("Error al analizar el JSON:", e)
    except Exception as e:
        print("Error:", e)


class EventParser:
    def parse(self, json_data):
        return parse_event(json_data)

    pass


class EventType(Enum):
    MESSAGE_CREATED = "message_created"
    UNKNOWN = "unknown"


class EventPayload(BaseModel):
    # event type,  payload is de json data
    event: str
    event_type: Optional[EventType] = None
    payload: dict = {}
    message_created_form: Optional[MessageCreatedForm] = None

    def __init__(self, event: str, payload: str):
        super().__init__(event=event, payload=payload)
        print("Event:", event)
        try:
            self.event_type = EventType(event)
        except ValueError:
            self.event_type = EventType.UNKNOWN

        if self.is_message_created():
            self.message_created_form = parse_message_created_event(payload)

    def is_message_created(self):
        return self.event_type == EventType.MESSAGE_CREATED

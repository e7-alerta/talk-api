from chatwoot import conversations_client
from chatwoot.types import ChatContact
from dash.types import DashPlaceInfo

from services.chat import greeting_maker


def create_conversation(contact: ChatContact):
    print("[ conversation_service::create_conversation ] ", contact)
    conversation = conversations_client.create(contact)
    print("[ conversation_service::create_conversation ] conversation created: ", conversation)
    return conversation


def send_message(conversation_id: str, message: str):
    print("[ conversation_service::send_message ] ", conversation_id, message)
    conversations_client.send_message(conversation_id, message)
    pass
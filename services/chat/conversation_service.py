from chatwoot import conversations_client
from chatwoot.types import ChatContact
from dash.types import DashPlaceInfo

from services.chat import greeting_maker


def create_conversation(contact: ChatContact):
    print("[ conversation_service::create_conversation ] ", contact)
    conversation = conversations_client.create(contact)
    print("[ conversation_service::create_conversation ] conversation created: ", conversation)
    return conversation


def send_message(contact: ChatContact, message: str):
    print("[ conversation_service::send_message ] ", contact, message)
    conversations_client.send_message(contact, message)
    pass
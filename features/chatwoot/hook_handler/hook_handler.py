import re

import chatbot
from features.chatwoot.hook_handler.types import EventRequest
from features.greeting.types import MessageIntent
from handlers import place_greeting_message_handler as dash_place_greeting_message_handler

from memory import conversations_cache as botpress_conversations
from memory import conversations_metadata as  conversations_metadata

from services.dash import dash_places_service, dash_contacts_service, dash_phones_service


def extract_phone_key(content) -> str:
    keyword = "🚨️🚨"
    index = content.find(keyword)
    if index != -1:
        return content[index + len(keyword): index + len(keyword) + 4]
    keyword = " 🚨 "
    index = content.find(keyword)
    if index != -1:
        return content[index + len(keyword): index + len(keyword) + 4]
    return None


def evaluate_message_intent(content):
    if "🚨️🚨" in content:
        return MessageIntent.VECINO_GREETING
    elif " 🚨 " in content:
        return MessageIntent.PLACE_GREETING
    else:
        return MessageIntent.UNKNOWN
    pass


class MessageCreatedEventWrapper:
    message_intent: MessageIntent = None
    event: EventRequest = None

    def __init__(self, event):
        self.event = event
        self.message_intent = evaluate_message_intent(event.content)

    @classmethod
    def of(cls, event_request):
        return cls(event_request)

    def get_content(self):
        return self.event.content

    def is_owner_greeting(self):
        return self.message_intent == MessageIntent.PLACE_GREETING

    def get_phone_code(self):
        phone_key = extract_phone_key(self.event.content)
        if phone_key is not None:
            return phone_key.replace("+", "")

    def get_phone_number(self):
        return self.event.sender.phone_number

    def get_sender_name(self):
        return self.event.sender.name

    def get_conversation_id(self):
        return self.event.conversation.id
        pass


class MessageCreatedHandler:

    # handle_message_created(event)
    def handle(self, event_request: EventRequest = None):
        print(
            f"[ chatwoot message created handler ] -> handle a {event_request.message_type} of {event_request.content_type}")
        message_created_event = MessageCreatedEventWrapper.of(event_request)

        if message_created_event.is_owner_greeting():
            print(f"[ chatwoot message created handler ] -> handle a greeting message from owner")
            phone_code = message_created_event.get_phone_code()

            # obtiene o crea el contacto por el phone number
            # actualiza la asociacion del contacto con el phone
            (dash_contact, newly_contact) = dash_place_greeting_message_handler.handle(
                message_created_event.get_phone_number(),
                message_created_event.get_sender_name(),
                message_created_event.get_phone_code()
            )

            dash_contact = dash_contacts_service.find_by_phone(message_created_event.get_phone_number())
            print(".......................", dash_contact)
            dash_place = dash_places_service.get_place(dash_contact["place"])

            # check if contact has a botpress user
            if dash_contact["botpress_id"] is None:
                # botpress_user_service.create_user(
                botpress_user = chatbot.create_user(
                    phone_number=dash_contact["phone"],
                    name=dash_contact["name"]
                )
                print("botpress user created ", botpress_user)
                # update contact with botpress_id
                dash_contacts_service.update_botpress_id(
                    contact_id=dash_contact["id"],
                    botpress_id=botpress_user["id"],
                )
                print("contact updated with botpress_id")
                botpress_user_id = botpress_user["id"]
            else:
                botpress_user_id = dash_contact["botpress_id"]


            # check if contact has a botpress conversation
            if dash_contact["botpress_conversation_id"] is None:
                (botpress_conversation, botpress_participant) = chatbot.create_conversation(
                    phone_number=dash_contact["phone"],
                    user_id=botpress_user_id,
                    conversation_id=f"{message_created_event.get_conversation_id()}"
                )
                print("botpress conversation created ", botpress_conversation)
                # update contact with botpress_conversation_id
                dash_contacts_service.update_botpress_conversation_id(
                    contact_id=dash_contact["id"],
                    botpress_conversation_id=botpress_conversation["id"]
                )
                print("contact updated with botpress_conversation_id")
                botpress_conversation_id = botpress_conversation["id"]
                pass
            else:
                botpress_conversation_id = dash_contact["botpress_conversation_id"]


            # create a bot conversation and cache it
            bot_conversation = chatbot.BotConversation(
                phone_number=dash_contact["phone"],
                name=dash_contact["name"],
                conversation_id=f"{botpress_conversation_id}",
                user_id=botpress_user_id,
                external_id=f"{message_created_event.get_conversation_id()}"
            )
            botpress_conversations.add_conversation(
                phone_number=message_created_event.get_phone_number(),
                conversation=bot_conversation
            )
            conversations_metadata[f"{botpress_conversation_id}"] = {
                "place_id": dash_contact["place"],
                "contact_id": dash_contact["id"],
                "chatwoot_conversation_id": f"{message_created_event.get_conversation_id()}",
                "sender_name": dash_contact["name"],
                "sender_profession": dash_contact["profession"],
                "place_name": None,
                "place_type": None,
                "place_street": dash_place.street,
                "place_street_number": dash_place.street_number,
                "botpress_conversation_id": f"{botpress_conversation_id}",
                "botpress_user_id": botpress_user_id,
                "payload": {},
            }

            bot_conversation.send_message(
                f"{message_created_event.get_content()}, me llamo {dash_contact['name']} y mi telefono es {dash_contact['phone']}"
            )




            # if botpress_conversations.has_conversation(phone_code):
            #     print("Enviando mensaje a conversacion existente")
            #     conversation = botpress_conversations.get_conversation_by_phone_number(phone_code)
            #     conversation.send_message(message_created_event.event.content)

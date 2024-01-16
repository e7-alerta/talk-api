
from fastapi import APIRouter, Request

from features.chatwoot.hook_handler import message_created_handler
from features.chatwoot.hook_handler.types import SenderType, ContentType, MessageType, EventType, EventRequest, MessageType, Conversation, ConversationMeta, Sender

chatwoot_routes = APIRouter()


@chatwoot_routes.post("/talk/v1/hooks/chatwoot/channel")
async def talk_chatwoot_channel(bodyForm: dict):
    print("[ talk_chatwoot_channel ] ", bodyForm)

    if bodyForm["event"] == "message_created":
        event = EventRequest(
            content_type=ContentType.of(bodyForm["content_type"]),
            content=bodyForm["content"],
            message_type=MessageType.of(bodyForm["message_type"]),
            event=EventType.MESSAGE_CREATED,
            conversation=Conversation(
                id=f"{bodyForm['conversation']['id']}",
            ),
            sender=Sender(
                name=bodyForm["sender"]["name"],
                phone_number=bodyForm["conversation"]["meta"]["sender"]["phone_number"],
                type=SenderType.of(bodyForm["conversation"]["meta"]["sender"]["type"])
            )
        )

        message_created_handler.handle(event)

    return {
        "status": "success",
        "message": "evento procesado"
    }

"""

    print("Event:", event)
    # si es un mensaje creado
    if event.is_message_created():

        if event.message_created_form is None:
            print("No es un mensaje de contacto")
            return {
                "status": "success",
                "message": "mensaje enviado"
            }

        message_form = event.message_created_form
        chatwoot_conversation_id = None
        if message_form.conversation_id is not None:
            chatwoot_conversation_id = message_form.conversation_id

        if not message_form.is_incoming():
            print("No es un mensaje entrante")
            return {
                "status": "success",
                "message": "mensaje enviado"
            }

        phone_number = int(message_form.phone_number.replace("+", ""))

        # check if in memory cache has a conversation with phone number
        if conversations_cache.has_conversation(phone_number):
            # send message to chatbot conversation
            print("Enviando mensaje a conversacion existente")
            conversation = conversations_cache.get_conversation_by_phone_number(phone_number)
            conversation.send_message(event.message_created_form.content)

        # si es un mensaje de contacto
        if event.message_created_form.is_vecino_greeting():
            print("Es un mensaje de saludo desde vecinos app")
            # contacts_manager.register_contact(event.message_created_form)
        elif event.message_created_form.is_place_greeting():
            print(
                "Es un mensaje de saludo desde place app por " + event.message_created_form.sender_name + " desde " + event.message_created_form.phone_number)
            (dash_contact, first_conversation) = place_greeting_message_handler.handle(event.message_created_form)
            print("dash_contact", dash_contact)
            print("first_conversation", first_conversation)

            dash_contact = dash_contacts_service.find_by_phone(event.message_created_form.phone_number)
            dash_place = dash_places_service.get_place(dash_contact["place"])
            print(dash_contact)

            user_id = None
            botpress_conversation_id = None

            if dash_contact["botpress_id"] is None:
                user = chatbot.create_user(
                    phone_number=dash_contact["phone"],
                    name=dash_contact["name"]
                )
                print("botpress user created ", user)
                # update contact with botpress_id
                dash_contacts_service.update_botpress_id(
                    contact_id=dash_contact["id"],
                    botpress_id=user["id"],
                )
                print("contact updated with botpress_id")
                user_id = user["id"]
            else:
                user_id = dash_contact["botpress_id"]

            if dash_contact["botpress_conversation_id"] is None:
                (conversation, participant) = chatbot.create_conversation(
                    phone_number=dash_contact["phone"],
                    user_id=user_id,
                    conversation_id=f"{chatwoot_conversation_id}"
                )
                print("botpress conversation created ", conversation)
                # update contact with botpress_conversation_id
                dash_contacts_service.update_botpress_conversation_id(
                    contact_id=dash_contact["id"],
                    botpress_conversation_id=conversation["id"]
                )
                print("contact updated with botpress_conversation_id")
                botpress_conversation_id = conversation["id"]
                pass
            else:
                botpress_conversation_id = dash_contact["botpress_conversation_id"]

            bot_conversation = chatbot.BotConversation(
                phone_number=dash_contact["phone"],
                name=dash_contact["name"],
                conversation_id=f"{botpress_conversation_id}",
                user_id=user_id,
                external_id=f"{chatwoot_conversation_id}"
            )
            # make a phone number to int remove "+" from phone number
            conversations_cache.add_conversation(phone_number, bot_conversation)
            conversations_metadata[f"{botpress_conversation_id}"] = {
                "place_id": dash_contact["place"],
                "contact_id": dash_contact["id"],
                "chatwoot_conversation_id": f"{chatwoot_conversation_id}",
                "sender_name": dash_contact["name"],
                "sender_profession": dash_contact["profession"],
                "place_name": None,
                "place_type": None,
                "place_street": dash_place.street,
                "place_street_number": dash_place.street_number,
                "botpress_conversation_id": f"{botpress_conversation_id}",
                "botpress_user_id": user_id,
                "payload": {},
            }

            bot_conversation.send_message(
                f"{event.message_created_form.content}, me llamo {dash_contact['name']} y mi telefono es {dash_contact['phone']}")

    return {
        "status": "success",
        "message": "mensaje enviado"
    }
"""

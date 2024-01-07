from fastapi import FastAPI

from memory import conversations_by_phone, contacts_by_phone, conversations_cache

from features.greeting.parser import EventPayload
from handlers import place_greeting_message_handler
from managers.types import CreateContactForm, SendPanicAlertForm
from managers import contacts_manager
from services.speak import speaker_service

from services.dash import contacts_service as dash_contacts_service

from features.greeting import event_handler, EventHandler

import chatbot

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Talk"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/talk/v1/talk/panic_alert")
async def talk_panic_alert(bodyForm: dict):
    print("[ talk_panic_alert ] ", bodyForm)
    form = SendPanicAlertForm(
        contact=bodyForm["contact"],
        place=bodyForm["place"]
    )

    contacts_manager.send_panic_alarm(contact=form.contact, place=form.place)
    speaker_service.send_panic_alert(contact=form.contact, place=form.place)

    return {
        "status": "success",
        "message": "mensaje enviado"
    }


@app.post("/talk/v1/hooks/chatwoot/channel")
async def talk_chatwoot_channel(bodyForm: dict):
    print("[ talk_chatwoot_channel ] ", bodyForm)

    event: EventPayload = event_handler.handle_event(bodyForm)

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

            user_id = None
            conversation_id = None
            # if contact not has botpress_id create a botpress user
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
                    conversation_id=dash_contact["last_conversation_id"]
                )
                print("botpress conversation created ", conversation)
                # update contact with botpress_conversation_id
                dash_contacts_service.update_botpress_conversation_id(
                    contact_id=dash_contact["id"],
                    botpress_conversation_id=conversation["id"]
                )
                print("contact updated with botpress_conversation_id")
                conversation_id = conversation["id"]
                pass
            else:
                conversation_id = dash_contact["botpress_conversation_id"]

            bot_conversation = chatbot.BotConversation(
                phone_number=dash_contact["phone"],
                name=dash_contact["name"],
                conversation_id=conversation_id,
                user_id=user_id,
                external_id=dash_contact["last_conversation_id"]
            )
            # make a phone number to int remove "+" from phone number
            conversations_cache.add_conversation(phone_number, bot_conversation)

            bot_conversation.send_message(
                f"{event.message_created_form.content}, me llamo {dash_contact['name']} y mi telefono es {dash_contact['phone']}")

            # create a chatbot conversation
            # conversation = chatbot.create_conversation( )

            # conversations_by_phone[event.message_created_form.phone_number] = conversation
            # send message to chatbot conversation
            # conversation.send_message(event.message_created_form.content)

    return {
        "status": "success",
        "message": "mensaje enviado"
    }


@app.post("/talk/v1/hooks/contacts/create")
async def talk_contacts_create(bodyForm: dict):
    print("[ talk_contacts_create ] ", bodyForm)

    keep_current_conversation = False
    if "keep_current_conversation" in bodyForm:
        keep_current_conversation = bodyForm["keep_current_conversation"]

    chatwoot_id = None
    # check if payload has chatwoot_id
    if "chatwoot_id" in bodyForm["payload"]:
        chatwoot_id = bodyForm["payload"]["chatwoot_id"]

    place_id = None
    # check if place is in payload
    if "place" in bodyForm["payload"]:
        place_id = bodyForm["payload"]["place"]

    contact_type = None
    # check if contact_type is in payload
    if "contact_type" in bodyForm["payload"]:
        contact_type = bodyForm["payload"]["contact_type"]

    form = CreateContactForm(
        dash_id=bodyForm["key"],
        phone=bodyForm["payload"]["phone"],
        name=bodyForm["payload"]["name"],
        contact_type=contact_type,
        place_id=place_id,
        chatwoot_id=chatwoot_id,
        keep_current_conversation=keep_current_conversation
    )

    contacts_manager.register_contact(form)

    return {
        "status": "success",
        "message": "contacto creado",
        "data": form
    }


@app.post("/talk/v1/hooks/botpress/hooks/onboarding_place/before_outgoing_hook")
async def botpress_hook_onboarding_place__before_outgoing(bodyForm: dict):
    print("[ botpress_hook_onboarding_place__before_outgoing ] ", bodyForm)

    if bodyForm["payload"]["type"] != "text":
        return {}

    conversation: chatbot.BotConversation = conversations_cache.get_conversation_by_conversation_id(bodyForm["conversationId"])
    if conversation is None:
        print("No se encontro una conversacion con el id ", bodyForm["conversationId"])
        return {
            "status": "success"
        }

    chatwoot_conversation_id = conversation.external_id
    print(" ................................................ ")
    contacts_manager.send_message(
        conversation_id=chatwoot_conversation_id,
        message=bodyForm["payload"]["text"]
    )

    return {
        "status": "success"
    }


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9020)

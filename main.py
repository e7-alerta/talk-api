from fastapi import FastAPI

from features.greeting.parser import EventPayload
from handlers import place_greeting_message_handler
from managers.types import CreateContactForm, SendPanicAlertForm
from managers import contacts_manager
from services.speak import speaker_service

from features.greeting import event_handler, EventHandler

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
        # si es un mensaje de contacto
        if event.message_created_form.is_vecino_greeting():
            print("Es un mensaje de saludo desde vecinos app")
            # contacts_manager.register_contact(event.message_created_form)
        elif event.message_created_form.is_place_greeting():
            print("Es un mensaje de saludo desde place app por " + event.message_created_form.sender_name + " desde " + event.message_created_form.phone_number)
            place_greeting_message_handler.handle(event.message_created_form)
            # contacts_manager.register_contact(event.message_created_form)

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

    return {
        "status": "success"
    }


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9020)

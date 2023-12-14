from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from managers.types import CreateContactForm, SendPanicAlertForm
from managers import contacts_manager
from services.speak import speaker_service

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


@app.post("/talk/v1/hooks/contacts/create")
async def talk_contacts_create(bodyForm: dict):
    print("[ talk_contacts_create ] ", bodyForm)

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
        chatwoot_id=chatwoot_id
    )

    contacts_manager.register_contact(form)

    return {
        "status": "success",
        "message": "contacto creado",
        "data": form
    }


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9020)

from fastapi import APIRouter, Request

from managers import contacts_manager
from managers.types import CreateContactForm

contacts_routes = APIRouter()


@contacts_routes.post("/talk/v1/hooks/contacts/create")
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

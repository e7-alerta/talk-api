from fastapi import APIRouter

from managers import contacts_manager
from managers.types import SendPanicAlertForm
from services.speak import speaker_service

alert_routes = APIRouter()


@alert_routes.post("/talk/v1/talk/panic_alert")
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

import os
from twilio.rest import Client

from dash.types import DashContact, DashPlaceInfo

ACCOUNT_SID = "ACfd290673ba69ccb1748912b28521ab8d"

AUTH_TOKEN = "cb0f9f4b36e2e577b8f88a5ae9cf51e5"

account_sid = ACCOUNT_SID  # os.environ['TWILIO_ACCOUNT_SID']
auth_token = AUTH_TOKEN  # os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)


def send_panic_alert(contact: DashContact, place: DashPlaceInfo):
    print("[ speaker_service::send_alert ] ", contact, place)
    message = make_panic_alert_message(
        contact_name=contact.name,
        place_owner=place.contact_name,
        place_name=place.name,
        place_address=place.address
    )

    call = client.calls.create(
        twiml=message,
        to=contact.phone,
        from_='+5491128835917'
    )
    print(call.sid)


def make_panic_alert_message(
        contact_name: str,
        place_owner: str,
        place_name: str,
        place_address: str,
):
    message = (
        f"<Response> <Say language=\"es-MX\" voice=\"man\" loop=\"1\" >"
        f"Buenas. <Pause length=\"3\"/>   {contact_name}."
        f"<Pause length=\"3\"/>  {place_owner} ha alertado desde el comercio \"{place_name}\" "
        f"<Pause length=\"3\"/>  ubicado enn {place_address}."
        "<Pause length=\"2\"/>  Ya estamos informando a las autoridades. "
        "<Pause length=\"3\"/> Te mantendremos informado."
        "<Pause length=\"3\"/> Gracias por utilizar nuestro servicio de alerta."
        "</Say></Response>",
    )
    return message

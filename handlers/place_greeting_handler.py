from datetime import datetime, timezone
from services.dash import contacts_service as dash_contacts_service
from services.dash import phones_service as dash_phones_service
from services.dash import places_service as dash_places_service


def _update_contact_associations(contact, phone_key):
    print("------------------------------------", contact)
    if not contact["phones"] or not contact["phones"][0].startswith(phone_key):

        phone = _find_and_update_phone(contact, phone_key)

        contact["phones"] = [phone.id]
        if phone.place:
            contact.place = phone.place
            _update_place(contact["place"], contact)


def _update_place(place_id, contact):
    place_info = dash_places_service.get_place(place_id)

    if not place_info.owner_contact:
        dash_places_service.update_place(place_info.id, {
            "contacto": f"{contact.name}",
            "phone": f"{contact.phone}",
            "owner_contact": f"{contact.id}"
        })
        pass


def _is_new_contact(contact):
    # Suponiendo que contact es el diccionario que proporcionaste
    contact_created_date_str = contact["date_created"]

    # Convierte la cadena de texto a un objeto datetime
    contact_created_date = datetime.fromisoformat(contact_created_date_str.replace('Z', '+00:00'))

    # Obtiene la zona horaria actual
    current_timezone = datetime.now().astimezone().tzinfo

    # Añade la información de la zona horaria a contact_created_date
    contact_created_date = contact_created_date.replace(tzinfo=timezone.utc)

    # Convierte contact_created_date a la misma zona horaria que la actual
    contact_created_date = contact_created_date.astimezone(current_timezone)

    # Calcula la diferencia en días
    days_difference = (datetime.now(tz=current_timezone) - contact_created_date).days
    return days_difference < 1


def _find_and_update_phone(contact, phone_key):
    print("phone_key", phone_key)
    phone = dash_phones_service.find_first_without_contact_and_id_start_with(phone_key)
    print("phone", phone)
    phone.contact = contact
    dash_phones_service.update_contact(phone.id, contact["id"])
    return phone


def _get_or_create_contact(phone_number, sender_name):
    contact = dash_contacts_service.find_by_phone(phone_number)
    if not contact:
        contact = dash_contacts_service.create_contact({
            "name": sender_name, "phone": phone_number
        })
    return contact


class PlaceGreetingMessageHandler:

    def __init__(self):
        pass

    def handle(self, phone_number, sender_name, phone_key):
        """
        Gestiona mensajes o solicitudes entrantes, asegurando el manejo adecuado de contactos,
        teléfonos asociados y lugares en el contexto de un sistema de mensajería o comunicación.

        Parámetros:
        - numero_telefono (str): El número de teléfono asociado al mensaje entrante.
        - nombre_remitente (str): El nombre del remitente o un valor predeterminado si no se proporciona.
        - clave_telefono (str): Una clave utilizada para identificar y procesar el mensaje entrante.

        Devoluciones:
        - dash_contact (dict): Información sobre el contacto después de manejar el mensaje.
        - recien_creado (bool): Una bandera que indica si el contacto se creó recientemente durante el proceso.
        """
        print(f"[ place gretting message handler ] {phone_number} {sender_name} {phone_key}")

        dash_contact = _get_or_create_contact(phone_number, sender_name)
        _update_contact_associations(dash_contact, phone_key)
        return dash_contact, _is_new_contact(dash_contact)

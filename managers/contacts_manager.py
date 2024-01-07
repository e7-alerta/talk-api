from datetime import time
from time import sleep

from chatwoot.types import ChatContact
from dash.types import DashPlaceInfo, DashContact
from managers.types import CreateContactForm
from services.chat import contacts_service as chat_contacts_service, greeting_maker
from services.chat import conversation_service as chat_conversations_service
from services.dash import contacts_service as dash_contacts_service
from services.dash import places_service as dash_places_service


# registrar un nuevo contacto o actualizarlo


def register_contact(form: CreateContactForm):
    # si el contacto ya existe, actualizarlo
    if form.chatwoot_id is not None:
        print("[ update_contact ] ", form)
        pass

    # check if contact with phone already exists
    chat_contact = chat_contacts_service.get_contact_by_phone(form.phone)
    print("[ get_contact_by_phone ] ", chat_contact)

    new_contact = False
    if chat_contact is None:
        new_contact = True
        print("[ create chat contact ] ", chat_contact)
        chat_contact = chat_contacts_service.create_contact(ChatContact(
            name=form.name,
            phone_number=form.phone
        ))
        print("[ chat contact created ] ", chat_contact)

        # create a conversation for the contact if it doesn't exist
        chat_contact = chat_conversations_service.create_conversation(chat_contact)
        pass
    else:
        print("[ chat contact already exists ] ", chat_contact)

        # find conversation by contact
        conversations = chat_contacts_service.get_contact_conversations(chat_contact.id)
        print("[ conversations ] ", conversations)
        if len(conversations) == 0:
            print("[ conversation doesn't exist ] ")
            conversation = chat_conversations_service.create_conversation(chat_contact)
            print("[ conversation created #1 ] ", conversation)
            chat_contact.last_conversation_id = conversation.id
            pass
        else:
            conversations_open = [conv for conv in conversations if conv["status"] == "open"]
            if len(conversations_open) == 0:
                print("[ open conversation doesn't exist ] ")
                conversation = chat_conversations_service.create_conversation(chat_contact)
                print("[ conversation created #2 ] ", conversation)
                chat_contact.last_conversation_id = conversation.id
                pass
            else:
                conversation = max(conversations_open, key=lambda x: x["last_activity_at"])
                # ultima convirsacion abierta
                print("[ last open conversation ] ", conversation)
                chat_contact.last_conversation_id = conversation["id"]
                pass
            pass

    # luego de obtener el contacto, o crearlo debemos actualizar el chatwoot_id
    dash_contacts_service.update_chatwoot_id(contact_id=form.dash_id, chatwoot_id=chat_contact.id,
                                             last_conversation_id=chat_contact.last_conversation_id)

    if form.place_id is None:
        # el contacto no tiene un lugar asignado, asignarle el lugar
        print("[ the contact doesn't have a place assigned ] ", chat_contact)
        return
    else:
        # enviar mensaje de bienvenida
        place = dash_places_service.get_place(form.place_id)
        if new_contact:
            send_welcome_message(chat_contact, place)
        else:
            send_welcome_back_message(chat_contact, place)

        # enviemos un mensaje recordando que puede agregar nuevos contactos de confianza a su tienda.
        if form.contact_type == "owner":
            # sleep 5 seconds
            sleep(5)
            send_add_contact_message(chat_contact, place)
            pass
        pass
    pass


def send_welcome_message(chat_contact: ChatContact, place: DashPlaceInfo):
    print("[ conversation_service::send_welcome_message ] ", chat_contact, place)
    message = greeting_maker.generar_mensaje(
        contact_name=chat_contact.name,
        place_owner=place.contact_name,
        place_name=place.name,
        place_address=place.address
    )
    print("[ conversation_service::send_welcome_message ] message: ", message)
    chat_conversations_service.send_message(chat_contact.last_conversation_id, message)
    return None


def send_welcome_back_message(chat_contact: ChatContact, place: DashPlaceInfo):
    print("[ conversation_service::send_welcome_back_message ] ", chat_contact, place)
    message = greeting_maker.generar_mensaje(
        contact_name=chat_contact.name,
        place_owner=place.contact_name,
        place_name=place.name,
        place_address=place.address
    )
    print("[ conversation_service::send_welcome_back_message ] message: ", message)
    chat_conversations_service.send_message(chat_contact.last_conversation_id, message)
    return None


def send_add_contact_message(chat_contact, place):
    print("[ conversation_service::send_add_contact_message ] ", chat_contact, place)
    message = greeting_maker.add_contact_remainder()
    chat_conversations_service.send_message(chat_contact.last_conversation_id, message)
    pass


def send_message(conversation_id: str, message: str):
    print("[ conversation_service::send_message ] ", conversation_id, message)
    chat_conversations_service.send_message(
        conversation_id=conversation_id,
        message=message
    )
    pass


def send_panic_alarm(contact: DashContact, place: DashPlaceInfo):
    print("[ conversation_service::send_panic_alarm ] ", contact, place)
    message = greeting_maker.panic_alarm_message(
        contact_name=contact.name,
        place_owner=place.contact_name,
        place_name=place.name,
        place_address=place.address
    )
    chat_conversations_service.send_message(contact.last_conversation_id, message)
    pass

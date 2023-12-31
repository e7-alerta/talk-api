from chatwoot import contacts_client
from chatwoot import conversations_client


def create_contact(contact):
    # check if contact with phone already exists
    print("[ contacts_service::create_contact ] ", contact)
    contact = contacts_client.create(contact)
    return contact


def get_contact_by_phone(phone):
    print("[ contacts_service::get_contact_by_phone ] ", phone)
    return contacts_client.find_by_phone(phone)


def get_contact_conversations(contact_id):
    print("[ contacts_service::get_contact_conversations ] ", contact_id)
    return conversations_client.find_by_contact(contact_id)

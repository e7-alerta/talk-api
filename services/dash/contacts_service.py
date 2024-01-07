from dash import dash_contacts_client


def create_contact(new_contact_form: dict):
    print("[ contacts_service::create_contact ] ", new_contact_form)
    contact = dash_contacts_client.create(new_contact_form)
    return contact


def update_chatwoot_id(contact_id, chatwoot_id, last_conversation_id):
    print("[ contacts_service::update_chatwoot_id ] ", contact_id, chatwoot_id, last_conversation_id)
    dash_contacts_client.update(contact_id=contact_id, payload={
        "chatwoot_id": f"{chatwoot_id}",
        "last_conversation_id": f"{last_conversation_id}"
    })
    pass


def update_botpress_id(contact_id, botpress_id):
    print("[ contacts_service::update_botpress_id ] ", contact_id, botpress_id)
    dash_contacts_client.update(contact_id=contact_id, payload={
        "botpress_id": f"{botpress_id}"
    })
    pass


def update_botpress_conversation_id(contact_id, botpress_conversation_id):
    print("[ contacts_service::update_botpress_conversation_id ] ", contact_id, botpress_conversation_id)
    dash_contacts_client.update(contact_id=contact_id, payload={
        "botpress_conversation_id": f"{botpress_conversation_id}"
    })
    pass



def find_by_phone(phone):
    print("[ contacts_service::find_by_phone ] ", phone)
    response = dash_contacts_client.find_one_by_phone(phone=phone)
    print("[ contacts_service::find_by_phone ] response: ", response)
    return response

from dash import dash_contacts_client


def update_chatwoot_id(contact_id, chatwoot_id, last_conversation_id):
    print("[ contacts_service::update_chatwoot_id ] ", contact_id, chatwoot_id, last_conversation_id)
    dash_contacts_client.update(contact_id=contact_id, payload={
        "chatwoot_id": f"{chatwoot_id}",
        "last_conversation_id": f"{last_conversation_id}"
    })
    pass

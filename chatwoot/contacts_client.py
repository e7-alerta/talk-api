import json
from typing import List, Tuple
from pydantic import BaseModel

from chatwoot import ChatwootParams
from chatwoot.types import ChatContact


class ContactsClient(object):
    def __init__(self, session, params: ChatwootParams):
        self.session = session
        self.account_id = params.account_id
        self.contacts_url = f"{params.base_url}/api/v1/accounts/{params.account_id}/contacts"

    def create(self, contact: ChatContact):
        print("ContactsClient.create | contact", contact)
        response = self.session.post(self.contacts_url, json={
            "name": contact.name,
            "email": "",
            "phone_number": contact.phone_number,
            "additional_attributes": {
                "description": "",
                "company_name": "",
                "country_code": "AR",
                "country": "Argentina",
                "city": "lanus",
                "social_profiles": {
                    "twitter": "",
                    "facebook": "",
                    "linkedin": "",
                    "github": "",
                    "instagram": ""
                }
            }
        })

        print("ContactsClient.create | response", response.json())

        response.raise_for_status()
        # sample response is :
        """
            {'payload': {'contact': {'additional_attributes': {'description': '', 'company_name': '', 'country_code': 'AR', 'country': 'Argentina', 'city': 'lanus', 'social_profiles': {'twitter': '', 'facebook': '', 'linkedin': '', 'github': '', 'instagram': ''}}, 'availability_status': 'offline', 'email': None, 'id': 12, 'name': 'Ernesto simionato', 'phone_number': '+5491136206603', 'identifier': None, 'thumbnail': '', 'custom_attributes': {}, 'created_at': 1703249312, 'contact_inboxes': []}, 'contact_inbox': {'inbox': None, 'source_id': None}}}
        """
        # check if response is 200
        if response.status_code != 200:
            print("ContactsClient.create | response.status_code != 200", response)
            print(response.json())
            print(self.session.cookies)
            return None

        # check if payload has contact
        if "contact" not in response.json()["payload"]:
            print("ContactsClient.create | payload has no contact")
            return None

        # check if contact has id
        if "id" not in response.json()["payload"]["contact"]:
            print("ContactsClient.create | contact has no id")
            return None

        contact.id = response.json()["payload"]["contact"]["id"]
        print("ContactsClient.create | contact.id", contact.id)
        return contact

    def update(self, contact_id, contact):
        url = f'https://chatwoot.com/api/v1/contacts/{contact_id}'
        response = self.session.put(url, json=contact)
        response.raise_for_status()
        return response.json()

    def delete(self, contact_id):
        url = f'https://chatwoot.com/api/v1/contacts/{contact_id}'
        response = self.session.delete(url)
        response.raise_for_status()
        return response.json()

    def list(self):
        url = 'https://chatwoot.com/api/v1/contacts'
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get(self, contact_id):
        url = f'https://chatwoot.com/api/v1/contacts/{contact_id}'
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def find_by_phone(self, phone):
        # remove + from phone
        phone = phone.replace("+", "")
        url = f"{self.contacts_url}/filter?include_contact_inboxes=false&page=1&sort=name"
        payload = {
            "payload": [
                {
                    "attribute_key": "phone_number",
                    "filter_operator": "equal_to",
                    "attribute_model": "standard",
                    "custom_attribute_type": "",
                    "values": [phone]
                }
            ]
        }
        response = self.session.post(url, json=payload)
        # check if not response is 200
        if response.status_code != 200:
            print("ContactsClient.find_by_phone | response.status_code != 200", response)
            print(response.json())
            print(self.session.cookies)
            return None

        # check if payload is empty
        if len(response.json()["payload"]) == 0:
            print("ContactsClient.find_by_phone | payload is empty")
            return None

        # check if has meta.count == 0 no se encontro el contacto
        if response.json()["meta"]["count"] == 0:
            print("ContactsClient.find_by_phone | meta.count == 0")
            return None

        print(response.json())
        data = response.json()["payload"][0]
        print(f"chatwoot contacts client | contact finded is {data}")
        # return the first contact with a Contact object
        # change int id to str

        return ChatContact(
            id=str(data["id"]),
            name=data["name"],
            phone_number=data["phone_number"]
        )


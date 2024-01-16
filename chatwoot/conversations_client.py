import requests as requests

from chatwoot import ChatwootParams
from chatwoot.types import ChatContact


class ConversationsClient(object):

    def __init__(self, session, params: ChatwootParams):
        self.session = session
        self.account_id = params.account_id
        self.inbox_id = params.inbox_id
        # self.source_id = params.source_id
        self.conversations_url = f"{params.base_url}/api/v1/accounts/{params.account_id}/conversations"
        self.contacts_url = f"{params.base_url}/api/v1/accounts/{params.account_id}/contacts"

    def send_message(self, conversation_id: str, message: str):
        print("ConversationClient.send_message | contact", conversation_id)
        print("ConversationClient.send_message | message", message)
        payload = {
            "content": message,
            "private": False,
            "cc_emails": "",
            "bcc_emails": "",
            "to_emails": ""
        }
        # url = f"{self.conversations_url}/{conversation_id}/messages"
        url = "https://chat.vecinos.com.ar/api/v1/accounts/2/conversations/72/messages"

        print("ConversationClient.send_message | url", url, payload)


        # response = self.session.post( url, json=payload )

        headers = {
            # "cookie": "_chatwoot_session=5kQBaAz1UsCZUDQyrpdY5ho0mQtdtbOeIlHbZ0fxtQKwiU8nomOwtbMulr42HqigKoQUU8rageHd81WvrJgNUcavDn%252BCmv61Iv5gyMHc46WM9n1wPiSC83lZFZHhNuJQtPg9z18s9Nbr%252FTj8DfhJUT5l%252BnQ%252BuEYPmFrjv8QetvikhtJFRCh55namcuVTmVyE0e0pHLTa2xun0Ws%252FS%252FUInY2MxCyi0V%252FJCJEE8Y4XHISJFjP8kW14tR4ghj1IKoztHmucBlfaFMQWB2sBYLjDYqpjijQ%252F6h38iu3v3k8F63K2OyhBvBCeEGIcnWnTE4hTZNHLgyRFj6UEImRR2z%252BeRGEonjJSTZy%252BnLu2Cn6fMliLOFnyxnooPalUkRKLXMEbFppNUDcWqjZ0--kaaTvfHmIjLGTZ%252F5--ivvAxfmycyOg48j%252BwbAPgw%253D%253D",
            "authority": "chat.vecinos.com.ar",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "access-token": "D9cU_qEqhC_U3mrBzmuQiw",
            "client": "ABgy0tY2YXk1ax5LkXfiMg",
            "content-type": "application/json",
            "origin": "https://chat.vecinos.com.ar",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "token-type": "Bearer",
            "uid": "e7canasta@gmail.com"
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        print("ConversationClient.send_message | response.status_code", response.status_code)
        print("ConversationClient.send_message | response", response.json())
        response.raise_for_status()
        # check if id is in response
        pass

    def create(self, contact: ChatContact):
        print("ConversationClient.create | contact", contact)
        response = self.session.post(self.conversations_url, json={
            "contact_id": contact.id,
            "inbox_id": self.inbox_id,
            "source_id": contact.phone_number
        })

        print("ConversationClient.create | response", response.json())

        response.raise_for_status()

        if response.status_code != 200:
            print("ConversationClient.create | response.status_code != 200", response)
            print(response.json())
            print(self.session.cookies)
            return None

        # sample response is :
        """
        {'meta': {'sender': {'additional_attributes': {'city': 'lanus', 'country': 'Argentina', 'description': '', 'company_name': '', 'country_code': 'AR', 'social_profiles': {'github': '', 'twitter': '', 'facebook': '', 'linkedin': '', 'instagram': ''}}, 'availability_status': 'offline', 'email': None, 'id': 14, 'name': 'Ernesto simionato', 'phone_number': '+5491136206603', 'identifier': None, 'thumbnail': '', 'custom_attributes': {}, 'created_at': 1703298745}, 'channel': 'Channel::Api', 'hmac_verified': False}, 'id': 12, 'messages': [], 'account_id': 2, 'uuid': 'b3a198c7-37d6-48a7-9bc7-7c8d5c47dc6f', 'additional_attributes': {}, 'agent_last_seen_at': 0, 'assignee_last_seen_at': 0, 'can_reply': True, 'contact_last_seen_at': 0, 'custom_attributes': {}, 'inbox_id': 1, 'labels': [], 'muted': False, 'snoozed_until': None, 'status': 'open', 'created_at': 1703302043, 'timestamp': 1703302043, 'first_reply_created_at': 0, 'unread_count': 0, 'last_non_activity_message': None, 'last_activity_at': 1703302043, 'priority': None, 'waiting_since': 1703302043}
        
        """

        # check if id is in response
        if "id" not in response.json():
            print("ConversationClient.create | id not in response")
            return None

        contact.last_conversation_id = response.json()["id"]
        print("ConversationClient.create | conversation_id", contact.last_conversation_id)
        return contact

    def find_by_contact(self, contact_id):
        print("ConversationClient.find_by_contact | contact_id", contact_id)
        #  https://chat.vecinos.com.ar/api/v1/accounts/2/contacts/36/conversations
        response = self.session.get(f"{self.contacts_url}/{contact_id}/conversations")
        print("ConversationClient.find_by_contact | response.status_code", response.status_code)
        print("ConversationClient.find_by_contact | response", response.json())
        return response.json().get("payload", [])

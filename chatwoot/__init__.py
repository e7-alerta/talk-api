import requests

from chatwoot.params import ChatwootParams
from chatwoot.auth_client import AuthClient
from chatwoot.constants import USER_EMAIL, ACCESS_TOKEN, CLIENT, HASBRO
from chatwoot.contacts_client import ContactsClient
from chatwoot.conversations_client import ConversationsClient
from chatwoot.types import ChatContact

chatwoot_params = ChatwootParams(
    base_url="https://chat.vecinos.com.ar",
    account_id=2,
    inbox_id=1
)


session = requests.Session()

session.headers.update({
    'Accepts': 'application/json',
    'Content-Type': 'application/json',
})

session.headers.update({
    'uid': USER_EMAIL,
    'token/type': 'Bearer',
    'sec-fetch-mode': 'cors'
})

# session.headers.update({
#     'access-token': ACCESS_TOKEN,
#     'client': CLIENT
# })

auth_client = AuthClient(session, chatwoot_params)
"""
print(auth_client.session.cookies)
response = auth_client.login(USER_EMAIL, HASBRO)
if response:
    print(response["data"]["access_token"])
    session.headers.update({
        'access-token': response["data"]["access_token"],
        'client': CLIENT
    })
print(auth_client.session.cookies)
"""

# print("loging successful")

# conversations_client = ConversationsClient(session)


contacts_client = ContactsClient(
    auth_client.session,
    chatwoot_params
)

conversations_client = ConversationsClient(
    auth_client.session,
    chatwoot_params
)

if __name__ == '__main__':

    # create conversation
    conversation = conversations_client.create(
        ChatContact(
            id="14",
            name="Ernesto simionato",
            phone_number="+5491136206603"
        )
    )
    print("conversation", conversation)



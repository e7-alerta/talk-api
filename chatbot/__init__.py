import requests

PICTURE_URL = "https://play-lh.googleusercontent.com/ELzqzBwttLtcPd8tHMnoDcIW17CIaLVxuyCr-wAG_WV5bgAOkyuTMfZUteW-pybNmPY=s94-rw"

HEADERS = {
    "Content-type": "application/json",
    "Authorization": "Bearer bp_pat_pvCBMN9XdMZamMMQiT0g9e82pcAc12x432ud",
    "x-workspace-id": "wkspace_01HK5X8R49M6V8C79S2R1X4K0N",
    "x-bot-id": "61156f87-27ac-41f3-a7aa-c5d17b8629b6",
    "x-integration-id": "70261efe-3c3c-4dd8-97f1-7c158a81d6ee"
}


def create_user(phone_number, name):
    url = "https://api.botpress.cloud/v1/chat/users"

    payload = {
        "chanel": "channel",
        "name": name,
        "pictureUrl": PICTURE_URL,
        "tags": {"id": phone_number}
    }

    response = requests.request("POST", url, json=payload, headers=HEADERS)
    print(response.text)
    user = response.json()["user"]
    return user


def create_conversation(phone_number, user_id, conversation_id):
    print(f" creating conversation for {(phone_number, user_id, conversation_id)}")
    create_conversation_url = "https://api.botpress.cloud/v1/chat/conversations"
    payload = {
        "channel": "channel",
        "tags": {
            "id": conversation_id,
            "fromUserId": phone_number,
            "chatId": conversation_id
        }
    }
    response = requests.request("POST", create_conversation_url, json=payload, headers=HEADERS)
    print("........................................  conversation created  ........................................")
    print(response.text)
    conversation = response.json()["conversation"]
    conversation_id = conversation["id"]
    print("........................................    ........................................")

    add_participants_url = f"https://api.botpress.cloud/v1/chat/conversations/{conversation_id}/participants"
    payload = {"userId": user_id}
    response = requests.request("POST", add_participants_url, json=payload, headers=HEADERS)
    print("........................................  participant added  ........................................")
    print(response.text)
    participant = response.json()["participant"]
    print("................................................................................")

    return (conversation, participant)


def send_message(user_id, conversation_id, message, phone_number, external_conversation_id):
    print(f" sending {(user_id, conversation_id, message, phone_number, external_conversation_id)}")
    url = "https://api.botpress.cloud/v1/chat/messages"
    payload = {
        "userId": f"{user_id}",
        "conversationId": f"{conversation_id}",
        "payload": {
            "text": f"{message}"
        },
        "tags": {
            # "id": random.,
            #"fromUserId": f"{phone_number}",
            "chatId": f"{external_conversation_id}"
        },
        "type": "text"
    }
    response = requests.request("POST", url, json=payload, headers=HEADERS)
    print(response.text)
    message = response.json()["message"]
    return message


class BotConversation:

    def __init__(self, phone_number, name, conversation_id, user_id, external_id):
        self.phone_number = phone_number
        self.name = name
        self.conversation_id = conversation_id
        self.external_id = external_id
        self.user_id = user_id

    def send_message(self, message):
        print(f"[ chatbot self.phone_number ] sending {message}")
        return send_message(
            user_id = self.user_id,
            conversation_id=self.conversation_id,
            message = message,
            phone_number = self.phone_number,
            external_conversation_id=self.external_id
        )


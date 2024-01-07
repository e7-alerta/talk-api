from features.greeting.types import MessageCreatedForm
from services.dash import contacts_service as dash_contacts_service
from services.dash import phones_service as dash_phones_service


class PlaceGreetingMessageHandler:

    def __init__(self):
        pass

    def handle(self, message_form: MessageCreatedForm):
        (phone_number, sender_name, phone_key) = (
            message_form.phone_number,
            message_form.sender_name,
            message_form.phone_key
        )
        print(f"[ place gretting message handler ] {phone_number} {sender_name} {phone_key}")

        # check if contact with phone already exists
        first_conversation = False
        dash_contact = dash_contacts_service.find_by_phone(phone_number)
        print("[ dash contact ] ", dash_contact)

        if dash_contact is None:
            print("[ dash contact not found ] ")
            first_conversation = True
            if sender_name is None:
                sender_name = "Vecino"
                pass
            dash_contact = dash_contacts_service.create_contact({
                "name": sender_name,
                "phone": phone_number,
                "made_in_chat": True
            })
            print("[ dash contact created ] ", dash_contact)
            pass
        else:
            print("[ dash contact already exists ] ", dash_contact)
            pass

        # check if contact has a place associated
        if dash_contact["phones"] is None or len(dash_contact["phones"]) == 0:
            print("[ dash contact doesn't have a phones associated ] ")
            dash_phone = dash_phones_service.find_first_without_contact_and_id_start_with(phone_key)
            print("[ dash phones ] ", dash_phone)
            if dash_phone is not None:
                print("[ dash phone not found ] ")

                if dash_phone.phone_number is None:
                    print("[ dash phone doesn't have a phone number associated ] ", dash_phone)
                    dash_phone.phone_number = phone_number
                    print("[ dash phone number updated ] ", dash_phone)
                    dash_phones_service.update_phone_number(dash_phone.id, phone_number)
                    pass

                dash_phone.contact = dash_contact
                dash_phones_service.update_contact(dash_phone.id, dash_contact["id"])
                print("[ dash phone contact assigned ] ", dash_phone, dash_contact)
                dash_contact["phones"] = [dash_phone.id]
        else:
            print("[ dash contact has a phones associated ] ", dash_contact["phones"])
            phone_id = dash_contact["phones"][0]
            # check if phone id starts with phone_key
            if not phone_id.startswith(phone_key):
                print(f"[ dash phone doesn't start with phone_key #{phone_key} ] ", phone_id)
                pass
            pass

        return (dash_contact, first_conversation)

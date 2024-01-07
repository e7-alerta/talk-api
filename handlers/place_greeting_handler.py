from features.greeting.types import MessageCreatedForm


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

        contacts_service

        """
         know a sender of greeting place message:
          + ya es un contacto, buscarlo por phone number
          + no, crear el nuevo contacto con el nombre y el phone number, origen by chat.
          ---  
          + ya esta asociado a ese phone key, ver si el contacto esa asociado al phone
        """


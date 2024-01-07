from features.greeting.parser import EventParser, EventPayload
from features.greeting.types import MessageCreatedForm


def handle_message_created(form: MessageCreatedForm):
    print("Formulario:", form)


class EventHandler:

    def __init__(self):
        self.parser = EventParser()

    def handle_event(self, json_data):
        try:
            event: EventPayload = self.parser.parse(json_data)
            print("Event:", event)
            if event.is_message_created():
                handle_message_created(event.message_created_form)
            return event
        except Exception as e:
            print("Error:", e)


if __name__ == '__main__':
    json_contact_greeting = '''
    {
      "content_type": "text",
      "content": "👋🤗 Buenas noches, Alerta PBA  🚨️🚨056c",
      "conversation": {
        "meta": {
          "sender": {
            "phone_number": "+5491128835917",
            "type": "contact"
          }
        }
      },
      "message_type": "outgoing",
      "event": "message_created"
    }
    '''

    handler = EventHandler()
    handler.handle_event(json_contact_greeting)

    json_place_greeting = '''
    {
      "content_type": "text",
      "content": "Soy nuevo en Alerta PBA 🚨 056c",
      "conversation": {
        "meta": {
          "sender": {
            "phone_number": "+5491128835917",
            "type": "contact"
          }
        }
      },
      "message_type": "outgoing",
      "event": "message_created"
    }
    '''

    handler.handle_event(json_place_greeting)



from botpress.botpress_client import BotpressClient
from features.botpress.hook_handler.types import EventRequest


class HookHandler:

    def __init__(self, botpress_client: BotpressClient):
        self.botpress_client = botpress_client

    def handle(self, event: EventRequest):
        print("[ botpress_hook_handler ] event", event)
        # if event.event_name == "before_outgoing_middleware":
        #     return self.handle_before_outgoing_middleware(event)
        # elif event.event_name == "after_incoming_middleware":
        #     return self.handle_after_incoming_middleware(event)
        # else:
        #     return {}

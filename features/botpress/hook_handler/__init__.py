from botpress import botpress_client
from botpress.botpress_client import BotpressClient
from features.botpress.hook_handler.hook_handler import HookHandler

bootpress_client = BotpressClient()


hook_handler = HookHandler(botpress_client)
from chatbot import BotConversation

contacts_by_phone = [
]

conversations_by_phone = [
]


class ConversationCache:
    def __init__(self):
        self.cache_by_phone = {}
        self.cache = {}

    def add_conversation(self, phone_number, conversation: BotConversation):
        self.cache_by_phone[phone_number] = conversation
        self.cache[conversation.conversation_id] = conversation

    def get_conversation_by_phone_number(self, phone_number):
        if phone_number in self.cache_by_phone:
            return self.cache_by_phone[phone_number]
        else:
            return None

    def get_conversation_by_conversation_id(self, conversation_id):
        if conversation_id in self.cache:
            return self.cache[conversation_id]
        else:
            return None

    def has_conversation(self, phone_number):
        return phone_number in self.cache_by_phone


conversations_cache = ConversationCache()

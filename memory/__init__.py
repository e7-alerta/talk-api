from enum import Enum
from typing import Optional

from chatbot import BotConversation

from pydantic import BaseModel

contacts_by_phone = [
]

conversations_by_phone = [
]

conversations_metadata = {
}

workflows = {
}


class ContactInfo(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    phone_number: Optional[str] = None
    profession: Optional[str] = None
    contact_type: Optional[str] = None
    chatbot_contact_id: Optional[str] = None
    botpress_user_id: Optional[str] = None
    pass


class PlaceInfo(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    street: Optional[str] = None
    street_number: Optional[str] = None
    pass


class ConversationType(Enum):
    ONBOARDING_PLACE_OWNER = "onboarding_place_owner"
    pass


# class OnboardingPlaceOwnerStep(Enum):
class WorkflowStep(Enum):
    ONBOARDING_OWNER_PLACE__GREETING = "greeting"
    ONBOARDING_OWNER_PLACE__GET_USER_INFORMATION = "get_user_information"
    ONBOARDING_OWNER_PLACE__ASK_USER_INFORMATION = "ask_user_information"
    ONBOARDING_OWNER_PLACE__INFORM_USER_DATA = "inform_user_data"
    ONBOARDING_OWNER_PLACE__ASK_STORE_INFORMATION = "ask_store_information"
    ONBOARDING_OWNER_PLACE__VERIFIED_STORE_ADDRESS = "verified_store_address"
    ONBOARDING_OWNER_PLACE__INFORM_STORE_DATA = "inform_store_data"
    ONBOARDING_OWNER_PLACE__VERIFIED_STORE_DATA = "verified_store_data"
    ONBOARDING_OWNER_PLACE__SET_STORE_DATA = "set_store_data"
    ONBOARDING_OWNER_PLACE__ASK_EMERGENCY_CONTACTS = "ask_emergency_contacts"
    ONBOARDING_OWNER_PLACE__INFORM_EMERGENCY_CONTACTS = "inform_emergency_contacts"
    ONBOARDING_OWNER_PLACE__CONFIRM_EMERGENCY_CONTACTS = "confirm_emergency_contacts"
    ONBOARDING_OWNER_PLACE__TRANSFER_TO_AGENT = "transfer_to_agent"
    pass


class ConversationInfo(BaseModel):
    chatwoot_conversation_id: Optional[str] = None
    chatwoot_contact_id: Optional[str] = None
    botpress_conversation_id: Optional[str] = None
    botpress_user_id: Optional[str] = None
    pass


class ConversationContext(BaseModel):
    user: ContactInfo = None
    owner: ContactInfo = None
    place: PlaceInfo = None
    conversation: ConversationInfo = None
    contacts: dict = {}
    conversation_type: ConversationType = None
    current_step: WorkflowStep = None
    next_step: WorkflowStep = None
    pass


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

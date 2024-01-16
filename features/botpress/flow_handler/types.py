from enum import Enum
from typing import Dict, Any
from pydantic import BaseModel, Field


class FlowResponse(BaseModel):
    next_step: str = Field(..., alias="nextStep")
    data: Dict[str, Any] = Field(..., alias="data")


class FlowPayload(BaseModel):
    pass


class FlowStep(Enum):
    ONBOARDING_OWNER_PLACE__CLOSE_CONVERSATION = "close_conversation"
    ONBOARDING_OWNER_PLACE__SET_CONTACT_LIST = "set_contact_list"
    ONBOARDING_OWNER_PLACE__REQUEST_MEMBER_JOIN = "request_member_join"
    ONBOARDING_OWNER_PLACE__GREETING = "greeting"
    ONBOARDING_OWNER_PLACE__GET_USER_INFORMATION = "get_user_information"
    ONBOARDING_OWNER_PLACE__ASK_USER_INFORMATION = "ask_user_information"
    ONBOARDING_OWNER_PLACE__SET_USER_INFORMATION = "set_user_information"
    ONBOARDING_OWNER_LOAD_USER_AND_PLACE_INFO = "load_user_and_place_info"
    ONBOARDING_OWNER_PLACE__INFORM_USER_DATA = "inform_user_data"
    ONBOARDING_OWNER_PLACE__ASK_STORE_INFORMATION = "ask_store_information"
    ONBOARDING_OWNER_PLACE__VERIFIED_STORE_ADDRESS = "verified_store_address"
    ONBOARDING_OWNER_PLACE__SET_STORE_INFORMATION = "set_user_information"
    ONBOARDING_OWNER_PLACE__INFORM_STORE_DATA = "inform_store_data"
    ONBOARDING_OWNER_PLACE__VERIFIED_STORE_DATA = "verified_store_data"
    ONBOARDING_OWNER_PLACE__SET_STORE_DATA = "set_store_data"
    ONBOARDING_OWNER_PLACE__ASK_EMERGENCY_CONTACTS = "ask_emergency_contacts"
    ONBOARDING_OWNER_PLACE__INFORM_EMERGENCY_CONTACTS = "inform_emergency_contacts"
    ONBOARDING_OWNER_PLACE__CONFIRM_EMERGENCY_CONTACTS = "confirm_emergency_contacts"
    ONBOARDING_OWNER_PLACE__TRANSFER_TO_AGENT = "transfer_to_agent"
    pass

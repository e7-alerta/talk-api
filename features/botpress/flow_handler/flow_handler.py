from features.botpress.flow_handler.types import FlowPayload, FlowResponse, FlowStep
from memory import conversations_metadata, workflows, ContactInfo, PlaceInfo

from dash import dash_phones_client, dash_places_client, dash_contacts_client


class DashClient:
    pass


def get_user_information(
        user: ContactInfo,
        place: PlaceInfo
):
    print("flow_handler |  get_user_information:  ", user, place)
    return user, place


def get_place_information(place):
    print("flow_handler |  get_place_information:  ", place)
    return place


def set_user_information(user_name, user_profession):
    print("flow_handler |  set_user_information:  ", user_name, user_profession)
    dash_contacts_client.update_contact(
        contact_id=conversations_metadata["contact_id"],
        payload={
            "name": user_name
        }
    )
    pass


def set_store_information(place_name, place_type, place_street, place_street_number):
    print("flow_handler |  set_store_information:  ", place_name, place_type, place_street, place_street_number)
    pass


def set_contact_list(contacts):
    print("flow_handler |  set_contact_list:  ", contacts)
    pass


def request_member_join():
    print("flow_handler |  request_member_join:  ")
    pass


class FlowHandler:

    def __init__(
            self,
            dash_client: DashClient
    ):
        self.dash_client = dash_client
        pass

    def handle(
            chatbot_id: str = None,
            conversation_id: str = None,
            conversation_step: str = None,
            flow_payload: FlowPayload = None
    ) -> FlowResponse:
        conversation_context = workflows["0"]  # workflows[conversation_id]
        conversation_metadata = conversations_metadata[conversation_id]

        #########     GET_USER_INFORMATION      #########
        if FlowStep.ONBOARDING_OWNER_PLACE__GET_USER_INFORMATION.value == conversation_step:
            (user_name, place_info) = get_user_information(
                user=conversation_context.user,
                place=conversation_context.place
            )
            if place_info.address is None:
                return FlowResponse(
                    current_step=FlowStep.ONBOARDING_OWNER_PLACE__GET_USER_INFORMATION,
                    next_step=FlowStep.ONBOARDING_OWNER_PLACE__ASK_STORE_INFORMATION,
                    data={
                        "user_name": user_name,
                        "place_address": None,
                        "place_street": None,
                        "place_street_number": None
                    }
                )
            else:
                return FlowResponse(
                    current_step=FlowStep.ONBOARDING_OWNER_PLACE__GET_USER_INFORMATION,
                    next_step=FlowStep.ONBOARDING_OWNER_PLACE__VERIFIED_STORE_ADDRESS,
                    data={
                        "user_name": user_name,
                        "place_address": place_info.address,
                        "place_street": place_info.street,
                        "place_street_number": place_info.street_number
                    }
                )

        #########     SET_USER_INFORMATION      #########
        if FlowStep.ONBOARDING_OWNER_PLACE__SET_USER_INFORMATION.value == conversation_step:
            set_user_information(
                user_name=flow_payload["user_name"],
                user_profession=flow_payload["user_profession"],
            )
            place_info = get_place_information(
                place=conversation_context.place
            )
            if place_info.address is None:
                return FlowResponse(
                    current_step=FlowStep.ONBOARDING_OWNER_PLACE__SET_USER_INFORMATION,
                    next_step=FlowStep.ONBOARDING_OWNER_PLACE__ASK_STORE_INFORMATION,
                    data={
                        "place_name": None,
                        "place_type": None,
                        "place_address": None,
                        "place_street": None,
                        "place_street_number": None
                    }
                )
            else:
                return FlowResponse(
                    current_step=FlowStep.ONBOARDING_OWNER_PLACE__SET_USER_INFORMATION,
                    next_step=FlowStep.ONBOARDING_OWNER_PLACE__VERIFIED_STORE_ADDRESS,
                    data={
                        "place_name": place_info.name,
                        "place_type": place_info.type,
                        "place_address": place_info.address,
                        "place_street": place_info.street,
                        "place_street_number": place_info.street_number
                    }
                )

        #########     SET_STORE_INFORMATION      #########
        if FlowStep.ONBOARDING_OWNER_PLACE__SET_STORE_INFORMATION.value == conversation_step:
            set_store_information(
                place_name=flow_payload["place_name"],
                place_type=flow_payload["place_type"],
                place_street=flow_payload["place_street"],
                place_street_number=flow_payload["place_street_number"]
            )
            return FlowResponse(
                current_step=FlowStep.ONBOARDING_OWNER_PLACE__SET_STORE_INFORMATION,
                next_step=FlowStep.ONBOARDING_OWNER_PLACE__ASK_EMERGENCY_CONTACTS,
                data={}
            )

        #########     SET_CONTACT_LIST      #########
        if FlowStep.ONBOARDING_OWNER_PLACE__SET_CONTACT_LIST.value == conversation_step:
            set_contact_list(
                contacts=flow_payload["contacts"]
            )
            return FlowResponse(
                current_step=FlowStep.ONBOARDING_OWNER_PLACE__SET_CONTACT_LIST,
                next_step=FlowStep.ONBOARDING_OWNER_PLACE__REQUEST_MEMBER_JOIN,
                data={}
            )
            pass

        #########     REQUEST_MEMBER_JOIN   #########
        if FlowStep.ONBOARDING_OWNER_PLACE__REQUEST_MEMBER_JOIN.value == conversation_step:
            request_member_join()
            return FlowResponse(
                current_step=FlowStep.ONBOARDING_OWNER_PLACE__REQUEST_MEMBER_JOIN,
                next_step=FlowStep.ONBOARDING_OWNER_PLACE__CLOSE_CONVERSATION,
                data={}
            )
            pass

        return FlowResponse(
            current_step=FlowStep.ONBOARDING_OWNER_LOAD_USER_AND_PLACE_INFO,
            next_step=FlowStep.ONBOARDING_OWNER_PLACE__VERIFIED_STORE_ADDRESS,
            data={}
        )

from fastapi import APIRouter, Request

import chatbot
from managers import contacts_manager
from memory import conversations_cache, conversations_metadata, WorkflowStep, workflows

from services.dash import contacts_service as dash_contacts_service
from services.dash import places_service as dash_places_service

import features.botpress


botpress_routes = APIRouter()


def handle(context, conversation_step):
    # case for each workflow step
    if WorkflowStep.ONBOARDING_OWNER_PLACE__GREETING.value == conversation_step:
        print(" handle ONBOARDING_OWNER_PLACE__GREETING")
        pass
    elif WorkflowStep.ONBOARDING_OWNER_PLACE__GET_USER_INFORMATION.value == conversation_step:
        print(" handle ONBOARDING_OWNER_PLACE__GET_USER_INFORMATION | ", context.place)
        if context.place.address is None:
            return WorkflowStep.ONBOARDING_OWNER_PLACE__ASK_STORE_INFORMATION, {
                "user_name": context.user.name,
                "place_address": None,
                "place_street": None,
                "place_street_number": None
            }
        else:
            return WorkflowStep.ONBOARDING_OWNER_PLACE__VERIFIED_STORE_ADDRESS, {
                "user_name": context.user.name,
                "place_address": context.place.address,
                "place_street": context.place.street,
                "place_street_number": context.place.street_number
            }
    elif WorkflowStep.ONBOARDING_OWNER_PLACE__SET_STORE_DATA.value == conversation_step:
        print(" handle ONBOARDING_OWNER_PLACE__SET_STORE_DATA")
        dash_places_service.update_place(
            ""
        )
        return WorkflowStep.ONBOARDING_OWNER_PLACE__ASK_EMERGENCY_CONTACTS, {
        }
    else:
        print(" handle default")
        pass


@botpress_routes.post("/talk/v1/hooks/botpress/{chatbot_id}/conversation/{conversation_id}/step/{conversation_step}")
async def hook_botpress_conversation(chatbot_id: str, conversation_id: str, conversation_step: str,
                                     flow_payload: dict = {}):
    print("POST | hook botpress conversation |  ", (chatbot_id, conversation_id, conversation_step))

    context = workflows["0"]
    (next_step, data) = handle(context, conversation_step)
    print("next_step", next_step, "data", data)

    return {
        "status": "success",
        "version": "1.0",
        "currentStep": "load-user-and-place-info",
        "nextStep": next_step,
        "data": data
    }


@botpress_routes.post("/talk/v1/hooks/botpress/onboarding_place/before_outgoing_hook")
async def botpress_hook_onboarding_place__before_outgoing(bodyForm: dict):
    print("[ botpress_hook_onboarding_place__before_outgoing ] ", bodyForm)
    conversation_id = bodyForm["conversationId"]
    metadata = conversations_metadata[conversation_id]

    print("", bodyForm["payload"])

    if bodyForm["payload"]["type"] != "text":
        return {}

    data = bodyForm["data"]

    sender_name_chaged = False
    sender_profession_changed = False
    place_address_changed = False
    place_name_changed = False
    place_type_changed = False

    if "user_name" not in data or data["user_name"] is None or data["user_name"] == "":
        data["user_name"] = metadata["sender_name"]
    else:
        if metadata["sender_name"] != data["user_name"]:
            sender_name_chaged = True
            metadata["sender_name"] = data["user_name"]
            pass

    if "user_profession" not in data or data["user_profession"] is None or data["user_profession"] == "":
        if metadata["sender_profession"] is not None:
            data["user_profession"] = metadata["sender_profession"]
            pass
    else:
        if metadata["sender_profession"] != data["user_profession"]:
            sender_profession_changed = True
            metadata["sender_profession"] = data["user_profession"]
            pass

    if "place_address" not in data and data["place_address"] is None or data["place_address"] == "":
        data["place_street"] = metadata["street"]
        data["place_street_number"] = metadata["street_number"]
    else:
        if metadata["place_street"] != data["place_street"]:
            place_address_changed = True
            metadata["street"] = data["place_street"]
            metadata["street_number"] = data["place_street_number"]
            pass

    if "place_name" not in data and data["place_name"] is None or data["place_name"] == "":
        if metadata["place_name"] is not None:
            data["place_name"] = metadata["place_name"]
            pass
    else:
        if metadata["place_name"] != data["place_name"]:
            place_name_changed = True
            metadata["place_name"] = data["place_name"]
        pass

    if "place_type" not in data and data["place_type"] is None or data["place_type"] == "":
        if metadata["place_type"] is not None:
            data["place_type"] = metadata["place_type"]
            pass
    else:
        if metadata["place_type"] == data["place_type"]:
            place_type_changed = True
            metadata["place_type"] = data["place_type"]
        pass

    if place_address_changed or place_name_changed or place_type_changed:
        print("[ botpress_hook_onboarding_place__before_outgoing ] updating place ", (
            metadata["place_name"],
            metadata["place_type"],
            metadata["place_street"],
            metadata["place_street_number"]
        ))

        dash_places_service.update_place(metadata["place_id"], {
            "name": metadata["place_name"],
            "place_rubro": metadata["place_type"],
            "street": metadata["place_street"],
            "street_number": metadata["place_street_number"]
        })
        pass

    if sender_name_chaged or sender_profession_changed:
        print("[ botpress_hook_onboarding_place__before_outgoing ] updating contact ", (
            metadata["sender_name"],
            metadata["sender_profession"]
        ))

        dash_contacts_service.update_contact(metadata["contact_id"], {
            "name": metadata["sender_name"],
            "profession": metadata["sender_profession"]
        })
        pass

    conversation: chatbot.BotConversation = conversations_cache.get_conversation_by_conversation_id(
        conversation_id
    )

    if conversation is None:
        print("No se encontro una conversacion con el id ", bodyForm["conversationId"])
        return {
            "status": "success"
        }

    chatwoot_conversation_id = conversation.external_id
    print(" ................................................ ")
    contacts_manager.send_message(
        conversation_id=chatwoot_conversation_id,
        message=bodyForm["payload"]["text"]
    )

    return {
        "status": "success",
        "metadata": metadata
    }

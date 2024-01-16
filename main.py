from fastapi import FastAPI


from memory import workflows, WorkflowStep, ConversationType, ContactInfo, PlaceInfo, ConversationInfo, ConversationContext
from web.routes import alert_routes, contacts_routes, chatwoot_routes, botpress_routes

app = FastAPI()

app.include_router(alert_routes)
app.include_router(contacts_routes)
app.include_router(chatwoot_routes)
app.include_router(botpress_routes)


@app.get("/")
async def root():
    return {"message": "Hello Talk"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


workflows["0"] = ConversationContext(
    conversation_type=ConversationType.ONBOARDING_PLACE_OWNER,
    next_step=WorkflowStep.ONBOARDING_OWNER_PLACE__GREETING,
    current_step=WorkflowStep.ONBOARDING_OWNER_PLACE__GREETING,
    converation=ConversationInfo(
        chatwoot_conversation_id="1",
        chatwoot_contact_id="1",
        botpress_conversation_id="1",
        botpress_user_id="1"
    ),
    user=ContactInfo(
        name="Juan Perez",
        phone_number="+5491136206603",
        chatbot_contact_id="1",
        botpress_user_id="1"
    ),
    owner=ContactInfo(
        name="Juan Perez",
        phone_number="+5491136206603",
        chatbot_contact_id="1",
        botpress_user_id="1"
    ),
    place=PlaceInfo(
        id="1",
        name="Carpinteria de Juan",
        street="2794",
        street_number="0",
        address="2794,, Cno. Gral. Manuel Belgrano 2702, Villa Dominico, Provincia de Buenos Aires, Argentina",
    )
)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9025)

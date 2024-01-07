from dash import dash_phones_client
from dash.types import DashPhoneInfo


def update_contact(phone_id, contact_id):
    print("[ phones_service::update_contact ] ", phone_id, contact_id)
    dash_phones_client.update(phone_id=phone_id, payload={
        "contact": f"{contact_id}"
    })
    pass


def update_phone_number(phone_id, phone_number):
    print("[ phones_service::update_phone_number ] ", phone_id, phone_number)
    dash_phones_client.update(phone_id=phone_id, payload={
        "phone_number": f"{phone_number}"
    })
    pass


def find_first_without_contact_and_id_start_with(phone_key) -> DashPhoneInfo:
    print("[ phones_service::find_first_without_contact_and_id_start_with ] ", phone_key)
    phones = dash_phones_client.find_all_without_contact()
    if phones is None:
        print("[ phones_service::find_first_without_contact_and_id_start_with ] phone not found")
        return None
    for phone in phones:
        if phone["id"].startswith(phone_key):
            print("[ phones_service::find_first_without_contact_and_id_start_with ] phone found: ", phone)
            phone_info = DashPhoneInfo(
                id=phone["id"],
                phone_number=phone["phone_number"]
            )
            if phone["contact"] is not None:
                phone_info.contact = {
                    "id": phone["contact"]
                }
                pass
            if phone["place"] is not None:
                phone_info.place = {
                    "id": phone["place"]
                }
                pass
            return phone_info
        pass
    return None
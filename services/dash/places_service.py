from dash import dash_places_client
from dash.types import DashPlaceInfo


def get_place(place_id) -> DashPlaceInfo:
    print("[ places_service::get ] ", place_id)
    raw = dash_places_client.get(place_id=place_id)
    if raw is None:
        print("[ places_service::get ] place not found")
        return None
    return DashPlaceInfo(
        id=raw["id"],
        name=raw["name"],
        address=f"{raw['street']} {raw['street_number']}",
        street=raw["street"],
        street_number=f"{raw['street_number']}",
        contact_phone=raw["phone"],
        contact_name=raw["contacto"],
        owner_contact=raw["owner_contact"],
    )




def update_place(place_id: str = None, data: dict = {}):
    print("[ places_service::update_place ] ", place_id, data)
    dash_places_client.update(place_id=place_id, payload=data)
    pass

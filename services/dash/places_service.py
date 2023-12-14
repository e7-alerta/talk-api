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
        phone=raw["phone"],
        contact_name=raw["contacto"]
    )

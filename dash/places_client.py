import json
import requests

from dash.types import DashParams


class DashPlacesClient(object):

    def __init__(self, session, params: DashParams):
        self.session = session
        self.contacts_url = f"{params.base_url}/items/places"

    def get(self, place_id):
        url = "https://dash.vecinos.com.ar/items/places/" + place_id

        querystring = {}
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
        }

        response = self.session.request("GET", url, headers=headers)
        return response.json()["data"]

    def update(self, place_id, payload: dict):
        url = "https://dash.vecinos.com.ar/items/places/" + place_id

        querystring = {}
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
        }

        response = self.session.request("PATCH", url, json=payload, headers=headers)
        print(response.text)
        return response.json()["data"]

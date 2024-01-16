import json
import requests

from dash.types import DashParams


class DashContactsClient(object):

    def __init__(self, session, params: DashParams):
        self.session = session
        self.contacts_url = f"{params.base_url}/items/contacts"

    def create(self, payload: dict):
        url = "https://dash.vecinos.com.ar/items/contacts"
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
        }

        response = self.session.request("POST", url, json=payload, headers=headers)
        print(response.text)
        return response.json().get("data", {})

    def update(self, contact_id, payload: dict):
        url = "https://dash.vecinos.com.ar/items/contacts/" + contact_id
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
        }

        response = self.session.request("PATCH", url, json=payload, headers=headers)
        print(response.text)

    def find_one_by_phone(self, phone):
        url = "https://dash.vecinos.com.ar/items/contacts/"

        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
        }

        querystring = {
            "limit": "1",
            "filter[phone][_eq]": phone
        }
        #     "filter[status][_eq]": "active"

        response = self.session.request("GET", url, headers=headers, params=querystring)
        print(response.json())
        data = response.json().get("data", [])
        if len(data) == 0:
            return None
        return data[0]

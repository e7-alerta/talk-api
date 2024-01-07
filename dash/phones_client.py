import json
import requests

from dash.types import DashParams


class DashPhonesClient(object):

    def __init__(self, session, params: DashParams):
        self.session = session
        self.contacts_url = f"{params.base_url}/items/phones"

    def get(self, phone_id):
        url = "https://dash.vecinos.com.ar/items/phones/" + phone_id

        querystring = {}
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
        }

        response = self.session.request("GET", url, headers=headers)
        return response.json()["data"]

    def create(self, payload: dict):
        url = "https://dash.vecinos.com.ar/items/phones"
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
        }

        response = self.session.request("POST", url, json=payload, headers=headers)
        print(response.text)
        return response.json()

    def update(self, phone_id, payload: dict):
        url = "https://dash.vecinos.com.ar/items/phones/" + phone_id
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
        }

        response = self.session.request("PATCH", url, json=payload, headers=headers)
        print(response.text)

    def find_all_without_contact(self):
        url = "https://dash.vecinos.com.ar/items/phones/"

        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
        }

        querystring = {
            "limit": "100",
            "filter[contact][_null]": "true"
        }
        #     "filter[status][_eq]": "active"

        response = self.session.request("GET", url, headers=headers, params=querystring)
        print(response.json())
        data = response.json().get("data", [])
        return data

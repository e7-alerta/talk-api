import json

import requests

from dash.contacts_client import DashContactsClient
from dash.phones_client import DashPhonesClient
from dash.places_client import DashPlacesClient
from dash.types import DashParams

dash_params = DashParams(
    base_url="https://dash.vecinos.com.ar"
)

session = requests.Session()

session.headers.update({
    "accept": "application/json, text/plain, */*",
    "content-type": "application/json",
})


dash_contacts_client = DashContactsClient(
    session,
    dash_params
)

dash_places_client = DashPlacesClient(
    session,
    dash_params
)



dash_phones_client = DashPhonesClient(
    session,
    dash_params
)


if __name__ == '__main__':
    # find a place by id
    place = dash_places_client.get(place_id="cd6830eb-3144-411c-a75b-645a8fba6fc8")
    # print json tabulated
    print(json.dumps(place, indent=4))

    # dado un nombre de lugar su direccion el nombre de su propietario y su telefono

    # el mensaje deberiamos presentarnos como alerta pba una app de vecinos para la seguridad de la comunidad.
    # y el contacto nos lo informo el propietario del lugar para que le informemos ante una alerta de robo del lugar.
    # el mensaje deberia ser algo asi:
    # "Hola, soy un vecino de la comunidad de vecinos, te escribo para informarte que se ha activado una alerta de robo en tu lugar: {nombre del lugar} ubicado en {direccion del lugar}."


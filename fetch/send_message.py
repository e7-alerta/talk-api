import requests

url = "https://chat.vecinos.com.ar/api/v1/accounts/2/conversations/72/messages"

payload = {
    "content": "hola vecino",
    "private": False
}
headers = {
   # "cookie": "_chatwoot_session=5kQBaAz1UsCZUDQyrpdY5ho0mQtdtbOeIlHbZ0fxtQKwiU8nomOwtbMulr42HqigKoQUU8rageHd81WvrJgNUcavDn%252BCmv61Iv5gyMHc46WM9n1wPiSC83lZFZHhNuJQtPg9z18s9Nbr%252FTj8DfhJUT5l%252BnQ%252BuEYPmFrjv8QetvikhtJFRCh55namcuVTmVyE0e0pHLTa2xun0Ws%252FS%252FUInY2MxCyi0V%252FJCJEE8Y4XHISJFjP8kW14tR4ghj1IKoztHmucBlfaFMQWB2sBYLjDYqpjijQ%252F6h38iu3v3k8F63K2OyhBvBCeEGIcnWnTE4hTZNHLgyRFj6UEImRR2z%252BeRGEonjJSTZy%252BnLu2Cn6fMliLOFnyxnooPalUkRKLXMEbFppNUDcWqjZ0--kaaTvfHmIjLGTZ%252F5--ivvAxfmycyOg48j%252BwbAPgw%253D%253D",
    "authority": "chat.vecinos.com.ar",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "access-token": "D9cU_qEqhC_U3mrBzmuQiw",
    "client": "ABgy0tY2YXk1ax5LkXfiMg",
    "content-type": "application/json",
    "origin": "https://chat.vecinos.com.ar",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "token-type": "Bearer",
    "uid": "e7canasta@gmail.com"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
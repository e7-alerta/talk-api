import requests

url = "https://chat.vecinos.com.ar/api/v1/accounts/2/contacts/54"

payload = ""
headers = {
    "authority": "chat.vecinos.com.ar",
    "accept": "application/json, text/plain, */*",
    "access-token": "wgsAjNpeVESVFOATGQveuA",
    "client": "xa5H1vxL6Wqjei2UyG4kvA",
    "token-type": "Bearer",
    "uid": "e7canasta@gmail.com"
}

response = requests.request("GET", url, data=payload, headers=headers)

print(response.text)
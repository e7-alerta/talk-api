import requests

url = "https://chat.vecinos.com.ar/api/v1/accounts/2/conversations/72/messages"

querystring = {"before":"496"}

payload = ""
headers = {
    "cookie": "_chatwoot_session=%252FnoSg9MeWvmpNaW3c4eJ3ws9y09p8rw4NbWwYpI%252F1uhHLDMS0Xqz0%252BqnnV4gcigiBaxh%252FamFOqUETEPB22zYCf0aPUTUR1JZC4A8ThVu1xRrTxvuFM6TjGq9wc7agjTSNbn0R276Dk5jO0pI9PQAsNoxneN6D3coNVuzDPVNRiwZadc5zEAUGjeCvBDcQMj7Y3xPyVBWB5NqjzyZJWhq2imrypEZ8%252BL9lB9LwG6EpOhWWtwTp9aWzGnI7QBYQ6cIZZ23HWjZVxY%252FNMtqacscuXvccT3O5c2xj9VcoHxD8S6vEWYZY%252Fqb88ZfMob9kDqW4DiUJ39VfCElcCyXFeTywUYBMb0shZJEjxsRuipcOzEsEfavCQOIejR2QLVqfxGWIaskd0YEOhs1--jxP2ZV%252BCeCt2uV8a--NkYnSDqPPUT1ig7ViHughg%253D%253D",
    "accept": "application/json, text/plain, */*",
    "access-token": "wgsAjNpeVESVFOATGQveuA",
    "client": "xa5H1vxL6Wqjei2UyG4kvA",
    "token-type": "Bearer",
    "uid": "e7canasta@gmail.com"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

print(response.text)
import requests

url = "https://chat.vecinos.com.ar/api/v1/accounts/2/conversations"

payload = ""
# "cookie": "_chatwoot_session=Ukd1Bq21JNUcaGONO%252BC82xWyripdwJtC6NhBA8dakwGmQFCM3b9kyWi9LLG4KQcAUAJrhRdIKA9H0v2RuPhMrF4%252FjDkdczHSFQBXeqOCt%252FJgYaPUF06dHftGpAx6m1joU1GhfTfS%252FCixxdbsjDG2X%252BTHw3zk%252BQ%252BCznHPgO%252FWKgnSoeJ5PITYngWoT8KwWIm8OeERR2wQhf%252FGuQytgI1ggwVIe2WRHPGfBUpTCS98JUVNL5FH2bTNMzthFxymsdZXjWyGVUZV71b6jTcaXkU4lQ4HWe650lpWGXhXFC2agrNeL%252FdHZ%252FHoQcGp3aA1XiK4e%252FJg6shPJIqmRqtfkg5VqnqjMdaFTE3jjYDrljQy%252BjxTD%252Bpzd49h6yNN6xiCSA6TxH0uiY%252Bl9oWZ--mhlYyurqgiBu5KlE--4822CKPc0x8sbGqd%252B1gmWg%253D%253D",
headers = {
    "accept": "application/json, text/plain, */*",
    "access-token": "wgsAjNpeVESVFOATGQveuA",
    "client": "xa5H1vxL6Wqjei2UyG4kvA",
    "token-type": "Bearer",
    "uid": "e7canasta@gmail.com"
}

response = requests.request("GET", url, data=payload, headers=headers)

print(response.text)
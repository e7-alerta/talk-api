from pydantic import BaseModel

class ChatwootParams(BaseModel):
    base_url: str
    account_id: int
    inbox_id: int


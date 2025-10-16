from pydantic import BaseModel


class ResponseReturn(BaseModel):
    status: str
    user: dict
    timestamp: str
    fact: str

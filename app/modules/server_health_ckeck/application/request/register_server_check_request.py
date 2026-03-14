from pydantic import BaseModel


class RegisterServerCheckRequest(BaseModel):
    name: str
    command: str
    threshold: int
    operator: str
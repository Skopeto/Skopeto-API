from pydantic import BaseModel

class Registrator(BaseModel):
    id: str
    name: str
    password: str
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str]
    name: str
    email: str
    password: str

#aqui eu crio uma classe que é o modeloq ue o banco tem que seguir
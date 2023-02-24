from pydantic import BaseModel

class Logon(BaseModel):
    username: str
    pw: str
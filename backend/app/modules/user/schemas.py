from pydantic import BaseModel


class UserMeOut(BaseModel):
    id: int
    username: str
    email: str
    is_superuser: bool

from pydantic import BaseModel

class User(BaseModel):
    user_email: str
    disabled: bool

class UserInDB(User):
    hashed_password: str


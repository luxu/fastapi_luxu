from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    usename: str
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr

class UserDB(UserSchema):
    id: int
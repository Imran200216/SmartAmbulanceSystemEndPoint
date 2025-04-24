from pydantic import BaseModel, EmailStr, constr


class SignupRequestModel(BaseModel):
    username: constr(min_length=3)
    email: EmailStr
    password: constr(min_length=6)

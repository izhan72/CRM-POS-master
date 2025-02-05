from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    shopname: str
    phone_number: str
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

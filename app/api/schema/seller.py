from pydantic import BaseModel, EmailStr

class SellerCreateSchema(BaseModel):
    name:str
    email:EmailStr
    password:str
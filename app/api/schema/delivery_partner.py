from pydantic import BaseModel, EmailStr

class PartnerCreateSchema(BaseModel):
    name:str
    email:EmailStr
    password:str
    serviceable_zip_codes : list[int]
    max_handling_capacity: int 

class PartnerUpdateSchema(BaseModel):
    serviceable_zip_codes : list[int]
    max_handling_capacity: int

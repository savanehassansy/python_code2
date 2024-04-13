from pydantic import BaseModel,EmailStr, Field 
from typing import Optional
from datetime import datetime

class Users(BaseModel):
    name:str = Field(...)
    firstName:str = Field(...)
    username:str = Field(...)
    address: str = Field(...) 
    phone: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    verification_code: Optional[str] 
    expiration_time: Optional[datetime] 
    is_verified: Optional[bool] = False  
    class Config:
        schema_extra = {
            "example": {
                "name":"John",
                "firstName":"Doe",
                "username":"john14",
                "address": "cocody",
                "phone": "+2250787050192",
                "email": "savanehassansy09@gmail.com",
                "password": "Azerty@10"
            }
        }


class UserVerification(BaseModel):
    verification_code: str
    # expiration_time:str
    

def ResponseModel(data,status_code,message):
    return {
        "data": [data],
        "status_code": status_code,
        "message":message
    }

def ErrorResponseModel(error,status_code,message):
    return {
        "error": error,
        "status_code":status_code,
        "message":message
    }
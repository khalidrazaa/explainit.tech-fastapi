from pydantic import BaseModel, EmailStr, constr
from datetime import date

class AdminUserCreate(BaseModel):
    email: EmailStr
    phone: constr(min_length=10, max_length=15)
    full_name: str
    gender: constr(to_lower=True, regex="^(male|female|other)$")
    dob: date
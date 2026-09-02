from typing import Optional, Literal
from pydantic import BaseModel, EmailStr

class EmployeeInput(BaseModel):
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Literal["Male", "Female", "Other"]

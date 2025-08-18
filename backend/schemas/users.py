from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

# --- Reusable Validated Types ---
# Corrected MpinStr to enforce exactly 6 digits
MpinStr = Annotated[str, Field(min_length=4, max_length=6, pattern=r'^[0-9]{4,6}$')]
MobileNumber = Annotated[str, Field(min_length=10, max_length=10, pattern=r'^[0-9]{10}$')]
AadharNumber = Annotated[str, Field(min_length=12, max_length=12, pattern=r'^[0-9]{12}$')]


# --- User Schemas ---

# Schema for creating a new user (input)
class UserCreateSchema(BaseModel):
    f_name: str
    l_name: str
    email: EmailStr
    mpin: MpinStr
    password: str

# Schema for user login (input)
class UserLoginSchema(BaseModel):
    username: str = Field(...,alias="email")
    mpin: MpinStr
    password:str = None  # Optional, can be used for password-based login

# Schema for displaying user information safely (output)
class UserDisplaySchema(BaseModel):
    id: int
    f_name: str
    l_name: str
    email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)


# --- Account Schemas ---

# Schema for creating a new bank account (input)
class AccountCreateSchema(BaseModel):
    account_type: str
    mobile_number: MobileNumber
    aadhar_number: AadharNumber
    address: str

# Schema for displaying account information safely (output)
class AccountDisplaySchema(BaseModel):
    id: int
    account_number: str
    balance: float
    account_type: str

    model_config = ConfigDict(from_attributes=True)


# Schema for creating a new transaction (input)

class TransactionCreateSchema(BaseModel):
    account_id: int
    amount: float
    transaction_type: str
    description: Optional[str]=None



# Schema for displaying transaction information safely (output)
class TransactionDisplaySchema(BaseModel):
    id: int
    account_id: int
    amount: float
    transaction_type: str
    timestamp: str

    model_config = ConfigDict(from_attributes=True)




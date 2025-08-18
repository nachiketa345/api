from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field
from backend.schemas.users import MobileNumber,AadharNumber


ACCOUNT_NUMBER= Annotated[str, Field(min_length=14,max_length=14, pattern=r'^[A-Z0-9]{14}$')]
# Account Creating Schema
class AccountCreateSchema(BaseModel):
    account_type: str
    mobile_number: MobileNumber
    aadhar_number: AadharNumber
    address: str
    balance: float = 0.0  # Default balance set to 0.0

# Account Display Schema
class AccountDisplaySchema(BaseModel):
    id: int
    account_number: ACCOUNT_NUMBER
    account_type: str
    address: str
    balance: float

    model_config = ConfigDict(from_attributes=True)


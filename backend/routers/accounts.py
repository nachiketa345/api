import random, string
from typing import List
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from backend.auth import get_current_user
from backend.db import get_db
from backend.models import Account, User
from backend.schemas.accounts import AccountCreateSchema, AccountDisplaySchema


router=APIRouter(prefix="/accounts",tags=["Accounts"])

def generate_account_number():
    #14 character account number
    return ('SBIN' + ''.join(random.choices(string.digits, k=10)))


# Create a new bank account (Authenticated) (POST)

@router.post("/",response_model=AccountDisplaySchema,status_code=status.HTTP_201_CREATED)
def create_account(account:AccountCreateSchema,db:Session=Depends(get_db),
                   current_user: User=Depends(get_current_user)):
    acc_number=generate_account_number()

    #While loop to ensure unique account number and user
    #dont have to try manually the while loop will automatically
    #loop for the next one if a similar account number is founded
    while db.query(Account).filter(Account.account_number==acc_number).first():
        acc_number=generate_account_number()

    new_account=Account(
        user_id=current_user.id,           #Set by backend
        account_number=acc_number,
        account_type=account.account_type,
        mobile_number=account.mobile_number,
        aadhar_number=account.aadhar_number,
        address=account.address,
        balance=account.balance
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account



@router.get("/",response_model=List[AccountDisplaySchema])
def get_all_accounts(db:Session=Depends(get_db),
                     current_user: User=Depends(get_current_user)):
    return db.query(Account).filter(Account.user_id==current_user.id).all()


@router.get("/{account_id}",response_model=AccountDisplaySchema)
def get_account_by_id(account_id: int,db:Session=Depends(get_db),
                     current_user: User=Depends(get_current_user)):
    
    account=db.query(Account).filter(Account.id==account_id,
                                    Account.user_id==current_user.id).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Account not found")
    return account

#Update Account (PATCH)
@router.patch("/{account_id}",response_model=AccountDisplaySchema)
def update_account(account_id: int,account_update:AccountCreateSchema,db:Session=Depends(get_db),
                   current_user: User=Depends(get_current_user)):
    existing_account=db.query(Account).filter(Account.id==account_id,
                                              Account.user_id==current_user.id).first()
    
    if not existing_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Account not found")
    
    for field, value in account_update.dict(exclude_unset=True).items():
        setattr(existing_account,field,value)
    db.commit()
    db.refresh(existing_account)
    return existing_account


@router.delete("/{account_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int,db:Session=Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    existing_account=db.query(Account).filter(Account.id==account_id,
                                              Account.user_id==current_user.id).first()
    if not existing_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Account not found")
    db.delete(existing_account)
    db.commit()
from typing import List
from fastapi import APIRouter, Form, HTTPException,status,Depends
from sqlalchemy.orm import Session

from backend.auth import create_token_access, get_current_user, get_password_hash,verify_password
from backend.db import get_db
from backend.models import User
from backend.schemas.users import UserCreateSchema, UserDisplaySchema, UserLoginSchema


router=APIRouter(prefix="/users",tags=["Users"])

# Create new user (POST)

@router.post("/",response_model=UserDisplaySchema,status_code=status.HTTP_201_CREATED)
def create_user(user:UserCreateSchema,db:Session=Depends(get_db)):
    if db.query(User).filter(User.email==user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Email already exists')
    
    #Hash the password using bcrypt
    hashed_password=get_password_hash(user.password)
    new_user=User(
        f_name=user.f_name,
        l_name=user.l_name,
        email=user.email,
        mpin=user.mpin,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#Fetch all Users (GET)
@router.get("/",response_model=List[UserDisplaySchema])
def fetch_all_users(db:Session=Depends(get_db),
                    current_user: User=Depends(get_current_user)):
    users=db.query(User).all()
    return users


# Fetch user by id (GET /id)

@router.get("/{id}",response_model=UserDisplaySchema)
def fetch_user_by_id(id: int,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
    return user


#Update User (PATCH)
@router.patch("/{id}",response_model=UserDisplaySchema)
def update_user(id: int, user_update: UserCreateSchema, db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user,field,value)
    db.commit()
    db.refresh(user)
    return user


#To delete a User (DELETE)
@router.delete("{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return None





#LOGIN ROUTE 

@router.post("/login")
def login_user(username: str= Form(...),password: str= Form(None), 
               mpin: str= Form(None), db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.email==username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
 # Allow login with either MPIN or password
    if mpin:
        if mpin!=db_user.mpin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid MPIN")
    elif password:
        if not verify_password(password,db_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Password")
        
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid login credentials")
    

    #Create JWT token

    access_token=create_token_access({"sub":db_user.email})
    return {"access_token":access_token,"token_type":"bearer"}


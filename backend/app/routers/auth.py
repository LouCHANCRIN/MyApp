from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..schemas import UserLogin, UserResponse, Token
from .. import models, utils, oauth2
from ..database import get_db

router = APIRouter(
    tags=["Authentication"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)

@router.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    if not user or not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Invalid credentials'
        )
        
    access_token = oauth2.create_access_token(data={'user_id': user.id, 'user_role': user.role})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/me', response_model=UserResponse)
def get_current_user(current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    user_content = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {id} does not exist'
        )
    return user_content
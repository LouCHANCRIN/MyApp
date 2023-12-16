from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..schemas import UserLogin, UserResponse, UserCreate
from .. import models
from ..database import get_db
from ..utils import hash

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.post('/', status_code=201, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash(user.password)
    try:
        user = models.User(email=user.email, username=user.username, password=hashed_password, role='admin')
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'This email address is already used'
        )
    return user


@router.get('/{id}', response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user_content = db.query(models.User).filter(models.User.id == id).first()
    if not user_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {id} does not exist'
        )
    return user_content

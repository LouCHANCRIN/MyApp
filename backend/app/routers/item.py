from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional


from ..schemas import ItemBase, ItemResponse
from .. import models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/items",
    tags=["Items"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[ItemResponse])
def get_items(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    items = db.query(models.Item).filter(models.Item.title.contains(search)).limit(limit).offset(skip).all()
    return items


@router.post('/create', status_code=201, response_model=ItemResponse)
def create_item(item: ItemBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print("OK")
    print(item)
    item = models.Item(**item.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    print("OK")
    return item


@router.get('/{id}', response_model=ItemResponse)
def get_item(id: int, db: Session = Depends(get_db)):
    item_content = db.query(models.Item).filter(models.Item.id == id).first()
    if not item_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Item {id} does not exist'
        )
    return item_content


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    item_query = db.query(models.Item).filter(models.Item.id == id)
    
    item = item_query.first()
    if item == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Item {id} does not exist'
        )

    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Not authorized to delete this item'
        )

    item_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_item(id: int, new_item: ItemBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    item_query = db.query(models.Item).filter(models.Item.id == id)

    item = item_query.first()
    if item == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Item {id} does not exist'
        )
        
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Not authorized to update this item'
        )

    item_query.update(new_item.dict(), synchronize_session=False)
    db.commit()

    return {"message": f"Item {id} was updated"}

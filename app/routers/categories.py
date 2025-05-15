from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models, database, auth

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.post("/", response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(database.my_session_local),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_category = db.query(models.Category).filter(models.Category.name == category.name).first()
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/", response_model=List[schemas.Category])
def get_categories(
    db: Session = Depends(database.my_session_local),
    current_user: models.User = Depends(auth.get_current_user)
):
    return db.query(models.Category).all()

@router.get("/{category_id}", response_model=schemas.Category)
def get_category(category_id: int,
                 db: Session = Depends(database.my_session_local),
                 current_user: models.User = Depends(auth.get_current_user)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category_update: schemas.CategoryCreate,
                   db: Session = Depends(database.my_session_local),
                   current_user: models.User = Depends(auth.get_current_user)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = category_update.name
    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}")
def delete_category(category_id: int,
                   db: Session = Depends(database.my_session_local),
                   current_user: models.User = Depends(auth.get_current_user)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"msg": "Category deleted"}

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import schemas, models, database, auth
from sqlalchemy import desc

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.post("/", response_model=schemas.Task)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(database.my_session_local),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_task = models.Task(**task.dict(), user_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[schemas.Task])
def get_tasks(
    db: Session = Depends(database.my_session_local),
    current_user: models.User = Depends(auth.get_current_user),
    status: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    is_completed: Optional[bool] = Query(None),
    sort_by: Optional[str] = Query("due_date"),
    sort_desc: Optional[bool] = Query(False),
    skip: int = 0,
    limit: int = 20
):
    query = db.query(models.Task).filter(models.Task.user_id == current_user.id)
    if status:
        query = query.filter(models.Task.status == status)
    if category_id:
        query = query.filter(models.Task.category_id == category_id)
    if is_completed is not None:
        query = query.filter(models.Task.is_completed == is_completed)
    if sort_by in ["due_date", "priority", "created_at"]:
        sort_col = getattr(models.Task, sort_by)
        query = query.order_by(desc(sort_col) if sort_desc else sort_col)
    tasks = query.offset(skip).limit(limit).all()
    return tasks

@router.get("/{task_id}", response_model=schemas.Task)
def get_task(task_id: int,
             db: Session = Depends(database.my_session_local),
             current_user: models.User = Depends(auth.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task_update: schemas.TaskUpdate,
                db: Session = Depends(database.my_session_local),
                current_user: models.User = Depends(auth.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int,
                db: Session = Depends(database.my_session_local),
                current_user: models.User = Depends(auth.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"msg": "Task deleted"}

@router.patch("/{task_id}/status", response_model=schemas.Task)
def update_task_status(task_id: int, status: str,
                      db: Session = Depends(database.my_session_local),
                      current_user: models.User = Depends(auth.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if status not in ["pending", "completed"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    task.status = status
    task.is_completed = (status == "completed")
    db.commit()
    db.refresh(task)
    return task

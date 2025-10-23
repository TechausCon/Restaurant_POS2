from fastapi import Depends, FastAPI, HTTPException
from typing import List
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .db import SessionLocal, init_db

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from .db import SessionLocal, init_db
from seed import seed_db

@app.on_event("startup")
def on_startup():
    init_db()
    seed_db()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/tables/", response_model=schemas.Table)
def create_table(table: schemas.TableCreate, db: Session = Depends(get_db)):
    return crud.create_table(db=db, table=table)

@app.get("/tables/", response_model=List[schemas.Table])
def read_tables(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tables = crud.get_tables(db, skip=skip, limit=limit)
    return tables

@app.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db=db, category=category)

@app.get("/categories/", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories

@app.post("/menu-items/", response_model=schemas.MenuItem)
def create_menu_item(item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    return crud.create_menu_item(db=db, item=item)

@app.get("/menu-items/", response_model=List[schemas.MenuItem])
def read_menu_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    menu_items = crud.get_menu_items(db, skip=skip, limit=limit)
    return menu_items

@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db=db, order=order)

@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@app.put("/orders/{order_id}", response_model=schemas.Order)
def update_order_status(order_id: int, status_update: schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
    return crud.update_order_status(db=db, order_id=order_id, status=status_update.status)

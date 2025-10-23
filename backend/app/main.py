from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status, WebSocket
from starlette.websockets import WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from typing import List
from sqlalchemy.orm import Session
from . import crud, models, schemas, security
from .db import SessionLocal, init_db
from seed import seed_db

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

import json
from fastapi.encoders import jsonable_encoder

manager = ConnectionManager()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    init_db()
    seed_db()

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to create users")
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to view users")
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to view users")
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/tables/", response_model=schemas.Table)
def create_table(table: schemas.TableCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to create tables")
    return crud.create_table(db=db, table=table)

@app.get("/tables/", response_model=List[schemas.Table])
def read_tables(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    tables = crud.get_tables(db, skip=skip, limit=limit)
    return tables

@app.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to create categories")
    return crud.create_category(db=db, category=category)

@app.get("/categories/", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories

@app.post("/menu-items/", response_model=schemas.MenuItem)
def create_menu_item(item: schemas.MenuItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to create menu items")
    return crud.create_menu_item(db=db, item=item)

@app.get("/menu-items/", response_model=List[schemas.MenuItem])
def read_menu_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    menu_items = crud.get_menu_items(db, skip=skip, limit=limit)
    return menu_items

@app.post("/orders/", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.WAITER]:
        raise HTTPException(status_code=403, detail="Not authorized to create orders")
    new_order = crud.create_order(db=db, order=order)
    await manager.broadcast(json.dumps(jsonable_encoder(new_order)))
    return new_order

@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@app.get("/orders/table/{table_id}", response_model=List[schemas.Order])
def read_orders_by_table(table_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    orders = db.query(models.Order).filter(models.Order.table_id == table_id).all()
    return orders

@app.put("/orders/{order_id}", response_model=schemas.Order)
async def update_order_status(order_id: int, status_update: schemas.OrderStatusUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.KITCHEN]:
        raise HTTPException(status_code=403, detail="Not authorized to update order status")
    updated_order = crud.update_order_status(db=db, order_id=order_id, status=status_update.status)
    await manager.broadcast(json.dumps(jsonable_encoder(updated_order)))
    return updated_order

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/bills/", response_model=schemas.Bill)
def create_bill(bill: schemas.BillCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.WAITER]:
        raise HTTPException(status_code=403, detail="Not authorized to create bills")
    return crud.create_bill(db=db, bill=bill)

@app.get("/bills/", response_model=List[schemas.Bill])
def read_bills(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    bills = crud.get_bills(db, skip=skip, limit=limit)
    return bills

@app.get("/bills/table/{table_id}", response_model=List[schemas.Bill])
def read_bills_by_table(table_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    bills = crud.get_bills_by_table(db, table_id=table_id)
    return bills

@app.put("/bills/{bill_id}", response_model=schemas.Bill)
def update_bill_status(bill_id: int, bill_update: schemas.BillStatusUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.WAITER]:
        raise HTTPException(status_code=403, detail="Not authorized to update bill status")
    return crud.update_bill_status(db=db, bill_id=bill_id, is_paid=bill_update.is_paid, payment_method=bill_update.payment_method)

@app.get("/analytics/sales", response_model=dict)
def get_sales_analytics(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to view analytics")
    bills = crud.get_bills(db)
    total_sales = sum(bill.total for bill in bills if bill.is_paid)
    return {"total_sales": total_sales, "total_bills": len(bills)}

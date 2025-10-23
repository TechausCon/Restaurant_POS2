from sqlalchemy.orm import Session
from . import models, schemas
from .security import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_tables(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Table).offset(skip).limit(limit).all()

def create_table(db: Session, table: schemas.TableCreate):
    db_table = models.Table(number=table.number, seats=table.seats)
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_menu_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MenuItem).offset(skip).limit(limit).all()

def create_menu_item(db: Session, item: schemas.MenuItemCreate):
    db_item = models.MenuItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(table_id=order.table_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    for item in order.items:
        db_order_item = models.OrderItem(**item.dict(), order_id=db_order.id)
        db.add(db_order_item)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order_status(db: Session, order_id: int, status: schemas.OrderStatus):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order

def get_bill(db: Session, bill_id: int):
    return db.query(models.Bill).filter(models.Bill.id == bill_id).first()

def get_bills(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Bill).offset(skip).limit(limit).all()

def get_bills_by_table(db: Session, table_id: int):
    return db.query(models.Bill).join(models.Order).filter(models.Order.table_id == table_id).all()

def create_bill(db: Session, bill: schemas.BillCreate):
    db_bill = models.Bill(total=bill.total)
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    for order_id in bill.order_ids:
        db.query(models.Order).filter(models.Order.id == order_id).update({"bill_id": db_bill.id})
    db.commit()
    return db_bill

def update_bill_status(db: Session, bill_id: int, is_paid: int, payment_method: schemas.PaymentMethod):
    db_bill = db.query(models.Bill).filter(models.Bill.id == bill_id).first()
    db_bill.is_paid = is_paid
    db_bill.payment_method = payment_method
    db.commit()
    db.refresh(db_bill)
    return db_bill

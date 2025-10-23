from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .models import UserRole, OrderStatus

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int

class MenuItemCreate(MenuItemBase):
    pass

class MenuItem(MenuItemBase):
    id: int

    class Config:
        orm_mode = True

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    items: List[MenuItem] = []

    class Config:
        orm_mode = True

class TableBase(BaseModel):
    number: int
    seats: int

class TableCreate(TableBase):
    pass

class Table(TableBase):
    id: int

    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    menu_item: MenuItem

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    table_id: int
    items: List[OrderItemCreate]

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    created_at: datetime
    status: OrderStatus
    items: List[OrderItem] = []

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

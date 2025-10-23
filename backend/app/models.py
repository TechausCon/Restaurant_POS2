from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    WAITER = "waiter"
    KITCHEN = "kitchen"

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole))

class Table(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True, index=True)
    seats = Column(Integer)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    items = relationship("MenuItem", back_populates="category")

class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="items")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("tables.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    items = relationship("OrderItem", back_populates="order")
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=True)

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    quantity = Column(Integer)
    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem")

class PaymentMethod(str, enum.Enum):
    CASH = "cash"
    CARD = "card"

class Bill(Base):
    __tablename__ = "bills"
    id = Column(Integer, primary_key=True, index=True)
    total = Column(Float)
    is_paid = Column(Integer, default=0)
    payment_method = Column(Enum(PaymentMethod), nullable=True)
    orders = relationship("Order")

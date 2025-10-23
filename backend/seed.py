from app.db import SessionLocal
from app.models import User, UserRole
from app.schemas import UserCreate, TableCreate, CategoryCreate, MenuItemCreate
from app.crud import create_user, create_table, create_category, create_menu_item

def seed_db():
    db = SessionLocal()

    # Check if the database is already seeded
    if db.query(User).first():
        db.close()
        return

    # Create users
    create_user(db, UserCreate(username="admin", password="admin", role=UserRole.ADMIN))
    create_user(db, UserCreate(username="waiter", password="waiter", role=UserRole.WAITER))

    # Create tables
    for i in range(1, 11):
        create_table(db, TableCreate(number=i, seats=4))

    # Create categories
    category1 = create_category(db, CategoryCreate(name="Vorspeisen"))
    category2 = create_category(db, CategoryCreate(name="Hauptgerichte"))
    category3 = create_category(db, CategoryCreate(name="Getränke"))

    # Create menu items
    create_menu_item(db, MenuItemCreate(name="Salat", description="Gemischter Salat", price=5.50, category_id=category1.id))
    create_menu_item(db, MenuItemCreate(name="Suppe", description="Tomatensuppe", price=4.50, category_id=category1.id))
    create_menu_item(db, MenuItemCreate(name="Schnitzel", description="Wiener Schnitzel mit Pommes", price=12.50, category_id=category2.id))
    create_menu_item(db, MenuItemCreate(name="Pizza", description="Pizza Salami", price=10.00, category_id=category2.id))
    create_menu_item(db, MenuItemCreate(name="Wasser", description="Stilles Wasser", price=2.50, category_id=category3.id))
    create_menu_item(db, MenuItemCreate(name="Cola", description="Coca Cola", price=3.00, category_id=category3.id))

    db.close()

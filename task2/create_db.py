import json
from models import Base, Item
from database import engine, SessionLocal  # Import SessionLocal from database.py

# Create tables
Base.metadata.create_all(bind=engine)

# Load data from JSON and insert into the database
def load_data():
    with open("/home/meditab/Desktop/ujas/task1/json_data.json", "r") as file:
        data = json.load(file)

    db = SessionLocal()
    for item in data:
        db_item = Item(
            id=item["id"],
            loc=item["loc"],
            userId=item["userId"],
            description=item["description"],
            price=item["price"],
            status=item["status"]
        )
        db.add(db_item)
    db.commit()
    db.close()

if __name__ == "__main__":
    load_data()
    print("Database created and data loaded.")

import json, uvicorn
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy import Column, Float, Integer, String, JSON, create_engine, text
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session, sessionmaker
import math
import os

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, index=True)
    loc = Column(JSON)  # Store location as a JSON field
    userId = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    status = Column(String, index=True)

# Define lifespan event handlers
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run during startup (same as on_event('startup'))
    print("Starting the application...")
    Base.metadata.create_all(bind=engine)

    # Check if the table exists
    db = SessionLocal()
    table_exists = db.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='items';")).fetchone()
    db.close()

    if table_exists:
        # If table exists, load the data from the JSON file
        print("Table 'items' exists. Loading/Updating data...")
        load_data()
    else:
        print("ERROR: Table 'items' was NOT created! Please check database configuration.")

    # Code to run during shutdown (same as on_event('shutdown'))
    yield
    print("Shutting down the application...")


app = FastAPI(lifespan=lifespan)

# SQLite database URL
DATABASE_URL = "sqlite:///./test.db"

# Create the SQLite engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to load data from the JSON file
def load_data():
    # Path to your JSON file
    json_file_path = "/home/meditab/Desktop/ujas/task1/json_data.json"

    # Check if the JSON file exists
    if not os.path.exists(json_file_path):
        raise HTTPException(status_code=404, detail="JSON file not found.")

    with open(json_file_path, "r") as file:
        data = json.load(file)

    db = SessionLocal()
    for item in data:
        # Check if the item already exists by ID
        existing_item = db.query(Item).filter(Item.id == item["id"]).first()

        if existing_item:
            # If item exists, skip or update it (here we update the existing record)
            existing_item.loc = item["loc"]
            existing_item.userId = item["userId"]
            existing_item.description = item["description"]
            existing_item.price = item["price"]
            existing_item.status = item["status"]
        else:
            # If item does not exist, create a new one
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


# ✅ 1. GET all items
@app.get("/get-items")
def get_items(
    userId: str = Query(None, description="Filter by user ID"),
    item_id: str = Query(None, description="Filter by item ID"),
    status: str = Query(None, description="Filter by status"),
    loc: str = Query(None, description="Filter by location in format [lat,lon]"),
    db: Session = Depends(get_db)
):
    if not any([userId, item_id, status, loc]):
        raise HTTPException(status_code=400, detail="No filter provided. Please specify userId, id, status, or loc.")

    query = db.query(Item)

    if userId:
        query = query.filter(Item.userId == userId)
    if item_id:
        query = query.filter(Item.id == item_id)
    if status:
        query = query.filter(Item.status == status)
    if loc:
        try:
            lat, lon = map(float, loc.strip("[]").split(","))
            query = query.filter(Item.loc == [lat, lon])
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid location format. Use [lat,lon]")

    items = query.all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found matching the given criteria.")

    return items

# ✅ 2. GET items sorted by price
@app.get("/sort-by-price")
def sort_items_by_price(order: str = "asc", db: Session = Depends(get_db)):
    if order == "asc":
        return db.query(Item).order_by(Item.price.asc()).all()
    return db.query(Item).order_by(Item.price.desc()).all()

# ✅ 3. GET items within a given radius
@app.get("/get-items-in-radius")
def get_items_in_radius(radius: float, latitude: float, longitude: float, db: Session = Depends(get_db)):
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    items = db.query(Item).all()

    if not items:
        raise HTTPException(status_code=404, detail="No items found matching the given criteria.")

    return [item for item in items if haversine(latitude, longitude, item.loc[0], item.loc[1]) <= radius]

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)

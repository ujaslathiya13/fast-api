from fastapi import FastAPI, HTTPException
import json
from typing import List, Optional
# from pydantic import BaseModel
import math

app = FastAPI()

json_data = {}

JSON_FILE_PATH = '/home/meditab/Desktop/ujas/task1/json_data.json'


# class Item(BaseModel):
#     id: str
#     loc: List[float]
#     userId: str
#     description: Optional[str] = None
#     price: float
#     status: str

# Loading JSON file
@app.on_event("startup")
async def load_json():
    global json_data
    try:
        with open(JSON_FILE_PATH, 'r') as file:
            json_data = json.load(file)
        print("JSON data loaded successfully.")
    except FileNotFoundError:
        print("Error: File not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON.")


# Sorting List by Price in Asc/Desc Order
@app.get("/sort-by-price/{order}")
async def sort_by_price(order: str):
    if order not in ['asc', 'desc']:
        return {"error": "Invalid order. Use 'asc' or 'desc'."}

    sorted_data = sorted(json_data, key=lambda x: x['price'], reverse=(order == 'desc'))

    return sorted_data


# Getting Single item by Id or Location
@app.get("/get-item")
async def get_item(id: Optional[str] = None, loc: Optional[str] = None):
    if id is not None:
        item = next((item for item in json_data if item["id"] == id), None)
    elif loc is not None:
        loc_coordinates = [float(coord) for coord in loc.split(",")]
        item = next((item for item in json_data if item["loc"] == loc_coordinates), None)
    else:
        raise HTTPException(status_code=400, detail="Either 'id' or 'location' must be provided.")

    if item:
        return item

    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/get-items")
async def get_items(status: Optional[str] = None, userId: Optional[str] = None):
    filtered_items = json_data

    if status:
        # Filter by status if provided
        filtered_items = [item for item in filtered_items if item["status"] == status]

    if userId:
        # Filter by userId if provided
        filtered_items = [item for item in filtered_items if item["userId"] == userId]

    if filtered_items:
        return filtered_items

    raise HTTPException(status_code=404, detail="No items found matching the specified criteria")


R = 6371.0


# Haversine formula to calculate the distance between two points on the Earth's surface (given by latitude and longitude)
def haversine(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    # Distance in kilometers
    return R * c


@app.get("/get-items-in-radius")
async def get_items_in_radius(radius: float, latitude: float, longitude: float):
    items_within_radius = []

    for item in json_data:
        item_lat, item_lon = item["loc"]

        # Calculate the distance from the item's location to the query location
        distance = haversine(latitude, longitude, item_lat, item_lon)

        # If the distance is within the radius, add the item to the results
        if distance <= radius:
            items_within_radius.append(item)

    if items_within_radius:
        return items_within_radius
    else:
        raise HTTPException(status_code=404, detail="No items found within the specified radius")

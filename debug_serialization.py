import json
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import date

# Define the schema exactly as in schemas.py
class TentBase(BaseModel):
    name: str
    brand: Optional[str] = None
    price: Optional[int] = None
    capacity: Optional[Decimal] = None
    weight_kg: Optional[Decimal] = None
    size_w: Optional[Decimal] = None
    size_d: Optional[Decimal] = None
    size_h: Optional[Decimal] = None
    pack_w: Optional[Decimal] = None
    pack_d: Optional[Decimal] = None
    pack_h: Optional[Decimal] = None
    material: Optional[str] = None
    purchase_date: Optional[date] = None

class Tent(TentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Simulate data from SQLAlchemy
data = {
    "id": 1,
    "name": "Test",
    "brand": "Brand",
    "price": 100,
    "capacity": Decimal("3.0"),
    "weight_kg": Decimal("2.5"),
    "size_w": Decimal("100"),
    "size_d": Decimal("100"),
    "size_h": Decimal("100"),
    "pack_w": Decimal("50"),
    "pack_d": Decimal("50"),
    "pack_h": Decimal("50"),
    "material": "Poly",
    "purchase_date": date(2024, 1, 1)
}

try:
    print("Testing Pydantic validation...")
    tent = Tent(**data)
    print("Pydantic validation success.")
    
    print("Testing JSON serialization...")
    json_data = tent.model_dump_json()
    print("JSON serialization success:")
    print(json_data)
except Exception as e:
    print(f"Error: {e}")

# Try to connect to actual DB and fetch one row
print("\nTesting actual DB fetch and serialization...")
try:
    import models
    import database
    from sqlalchemy.orm import Session
    db = database.SessionLocal()
    t = db.query(models.Tent).first()
    if t:
        print(f"Fetched Tent ID: {t.id}, Capacity: {t.capacity} (type: {type(t.capacity)})")
        schema_tent = Tent.model_validate(t)
        print("Schema validation successful.")
        print(schema_tent.model_dump_json())
    else:
        print("No tents found in DB.")
    db.close()
except Exception as e:
    import traceback
    traceback.print_exc()

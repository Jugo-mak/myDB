from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional
from decimal import Decimal

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

class TentCreate(TentBase):
    pass

class TentUpdate(BaseModel):
    name: Optional[str] = None
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

class TentAggregates(BaseModel):
    total_count: int
    avg_price: Optional[float] = None
    max_price: Optional[int] = None
    min_price: Optional[int] = None

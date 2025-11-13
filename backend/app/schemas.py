from pydantic import BaseModel
from typing import Optional
from datetime import date


class MedicineBase(BaseModel):
    name: str
    qty: int
    min_stock: int
    expiry_date: Optional[date]


class MedicineCreate(MedicineBase):
    pass


class MedicineUpdate(BaseModel):
    name: Optional[str]
    qty: Optional[int]
    min_stock: Optional[int]
    expiry_date: Optional[date]


class Medicine(MedicineBase):
    id: int

    class Config:
        orm_mode = True

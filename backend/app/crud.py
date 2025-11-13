from sqlalchemy.orm import Session
from datetime import date, timedelta
from . import models, schemas


def get_medicines(db: Session):
    return db.query(models.Medicine).order_by(models.Medicine.id).all()


def get_medicine(db: Session, med_id: int):
    return db.query(models.Medicine).filter(models.Medicine.id == med_id).first()


def create_medicine(db: Session, med: schemas.MedicineCreate):
    db_med = models.Medicine(
        name=med.name, qty=med.qty, min_stock=med.min_stock, expiry_date=med.expiry_date
    )
    db.add(db_med)
    db.commit()
    db.refresh(db_med)
    return db_med


def update_medicine(db: Session, med_id: int, med: schemas.MedicineUpdate):
    db_med = get_medicine(db, med_id)
    if med.name is not None:
        db_med.name = med.name
    if med.qty is not None:
        db_med.qty = med.qty
    if med.min_stock is not None:
        db_med.min_stock = med.min_stock
    if med.expiry_date is not None:
        db_med.expiry_date = med.expiry_date
    db.commit()
    db.refresh(db_med)
    return db_med


def delete_medicine(db: Session, med_id: int):
    db_med = get_medicine(db, med_id)
    if db_med:
        db.delete(db_med)
        db.commit()


def get_low_stock(db: Session):
    return db.query(models.Medicine).filter(models.Medicine.qty < models.Medicine.min_stock).all()

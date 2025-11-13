from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

from . import models, schemas, crud, database

app = FastAPI(title="pharma-copilot Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    database.init_db()


@app.get("/medicines", response_model=List[schemas.Medicine])
def list_medicines(db: Session = Depends(get_db)):
    return crud.get_medicines(db)


@app.post("/medicines", response_model=schemas.Medicine)
def create_medicine(med: schemas.MedicineCreate, db: Session = Depends(get_db)):
    return crud.create_medicine(db, med)


@app.put("/medicines/{med_id}", response_model=schemas.Medicine)
def update_medicine(med_id: int, med: schemas.MedicineUpdate, db: Session = Depends(get_db)):
    db_med = crud.get_medicine(db, med_id)
    if not db_med:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return crud.update_medicine(db, med_id, med)


@app.delete("/medicines/{med_id}")
def delete_medicine(med_id: int, db: Session = Depends(get_db)):
    if not crud.get_medicine(db, med_id):
        raise HTTPException(status_code=404, detail="Medicine not found")
    crud.delete_medicine(db, med_id)
    return {"ok": True}


@app.get("/predict")
def predict(sku: str, days: int = 7):
    # Return a fake forecast for demonstration
    today = datetime.utcnow().date()
    data = []
    base = 50
    for i in range(days):
        day = today + timedelta(days=i)
        value = max(0, base + (i - days // 2) * 3)
        data.append({"date": day.isoformat(), "forecast": value})
    return {"sku": sku, "forecast": data}


@app.post("/chat")
def chat_endpoint(payload: dict, db: Session = Depends(get_db)):
    # Very simple rule-based copilot. Accepts {"message": "..."}
    msg = payload.get("message", "").lower()
    if not msg:
        raise HTTPException(status_code=400, detail="message required")

    if "low stock" in msg:
        low = crud.get_low_stock(db)
        if not low:
            return {"reply": "No low-stock items."}
        lines = [f"{m.name} (qty={m.qty}, min={m.min_stock})" for m in low]
        return {"reply": "Low stock:\n" + "\n".join(lines)}

    if "predict" in msg:
        # naive: look for a medicine name in the message
        for med in crud.get_medicines(db):
            if med.name.lower() in msg:
                # call predict endpoint logic
                return predict(sku=str(med.id), days=7)
        return {"reply": "Couldn't find that medicine to predict."}

    return {"reply": "Sorry — I can report low stock or predict <name>."}

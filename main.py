from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

import models
import schemas
import database

app = FastAPI(title="Tents Database API")

# Create tables (if they don't exist, though we assume they do)
# models.Base.metadata.create_all(bind=database.engine)

@app.get("/tents", response_model=List[schemas.Tent])
def read_tents(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    tents = db.query(models.Tent).offset(skip).limit(limit).all()
    return tents

@app.get("/tents/stats", response_model=schemas.TentAggregates)
def get_tent_stats(db: Session = Depends(database.get_db)):
    count = db.query(func.count(models.Tent.id)).scalar()
    avg_price = db.query(func.avg(models.Tent.price)).scalar()
    max_price = db.query(func.max(models.Tent.price)).scalar()
    min_price = db.query(func.min(models.Tent.price)).scalar()
    
    return {
        "total_count": count,
        "avg_price": round(avg_price, 2) if avg_price else None,
        "max_price": max_price,
        "min_price": min_price
    }

@app.get("/tents/{tent_id}", response_model=schemas.Tent)
def read_tent(tent_id: int, db: Session = Depends(database.get_db)):
    db_tent = db.query(models.Tent).filter(models.Tent.id == tent_id).first()
    if db_tent is None:
        raise HTTPException(status_code=404, detail="Tent not found")
    return db_tent

@app.post("/tents", response_model=schemas.Tent)
def create_tent(tent: schemas.TentCreate, db: Session = Depends(database.get_db)):
    db_tent = models.Tent(**tent.model_dump())
    db.add(db_tent)
    db.commit()
    db.refresh(db_tent)
    return db_tent

@app.put("/tents/{tent_id}", response_model=schemas.Tent)
def update_tent(tent_id: int, tent: schemas.TentUpdate, db: Session = Depends(database.get_db)):
    db_tent = db.query(models.Tent).filter(models.Tent.id == tent_id).first()
    if db_tent is None:
        raise HTTPException(status_code=404, detail="Tent not found")
    
    update_data = tent.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tent, key, value)
    
    db.commit()
    db.refresh(db_tent)
    return db_tent

@app.delete("/tents/{tent_id}")
def delete_tent(tent_id: int, db: Session = Depends(database.get_db)):
    db_tent = db.query(models.Tent).filter(models.Tent.id == tent_id).first()
    if db_tent is None:
        raise HTTPException(status_code=404, detail="Tent not found")
    db.delete(db_tent)
    db.commit()
    return {"detail": "Tent deleted"}

from fastapi import FastAPI, Depends, HTTPException
from models import Hostel as HostelSchema
from database import SessionLocal, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()


database_models.base.metadata.create_all(bind=engine)

#  Hostel management (create, update, delete hostels).   

hostels = [
    HostelSchema(id=1, name="Hostel A", location="City X", occupancy=50, subscription='Free'),
    HostelSchema(id=2, name="Hostel B", location="City Y", occupancy=30, subscription='Basic'),
    HostelSchema(id=3, name="Hostel C", location="City Z", occupancy=40, subscription='Premium')
]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 


def init_db():
    db = SessionLocal()
    count = db.query(database_models.Hostel).count()
    
    if count == 0:
        for hostel in hostels:
            db.add(database_models.Hostel(**hostel.model_dump()))
    db.commit()
    
init_db()

@app.get("/hostels")
def get_all_hostels(db: Session = Depends(get_db)):
    hostels = db.query(database_models.Hostel).all()
    return hostels

@app.get("/hostels/{hostel_id}")
def get_hostel_by_id(hostel_id: int, db: Session = Depends(get_db)):
    hostel = db.query(database_models.Hostel).filter(database_models.Hostel.id == hostel_id).first()
    if hostel:
        return hostel
    raise HTTPException(status_code=404, detail="Hostel not found")

@app.post("/hostels")
def create_hostel(hostel: HostelSchema, db: Session = Depends(get_db)):
    db_hostel = database_models.Hostel(
        id=hostel.id,
        name=hostel.name,   
        location=hostel.location,
        occupancy=hostel.occupancy,
        subscription=hostel.subscription
    )
    db.add(db_hostel)
    db.commit()
    db.refresh(db_hostel)
    return db_hostel

@app.put("/hostels/{hostel_id}")
def update_hostel(hostel_id: int, updated_hostel: HostelSchema, db: Session = Depends(get_db)):
    hostel = db.query(database_models.Hostel).filter(database_models.Hostel.id == hostel_id).first()
    if hostel:
        hostel.name = updated_hostel.name
        hostel.subscription = updated_hostel.subscription
        hostel.occupancy = updated_hostel.occupancy
        db.commit()
        db.refresh(hostel)
        return hostel
    raise HTTPException(status_code=404, detail="Hostel not found")


@app.delete("/hostels/{hostel_id}")
def delete_hostel(hostel_id: int, db: Session = Depends(get_db)):
    hostel = db.query(database_models.Hostel).filter(database_models.Hostel.id == hostel_id).first()
    if hostel:
        db.delete(hostel)
        db.commit()
        return 'Hostel deleted successfully'
    raise HTTPException(status_code=404, detail="Hostel not found")
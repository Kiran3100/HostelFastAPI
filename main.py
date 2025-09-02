from fastapi import FastAPI
from models import Hostel
    

app = FastAPI()

hostels = [
    Hostel(id=1, name="Sunrise Hostel", subscription="Premium", occupancy=92.0),
    Hostel(id=2, name="Lakeview Hostel", subscription="Standard", occupancy=75.0),
    Hostel(id=3, name="Greenwood Hostel", subscription="Free", occupancy=61.0),
]   

@app.get("/hostels")
def get_all_hostels():
    return hostels

@app.get("/hostels/{hostel_id}")
def get_hostel_by_id(hostel_id: int):
    for hostel in hostels:
        if hostel.id == hostel_id:
            return hostel
    return 'Hostel not found'

@app.post("/hostels")
def create_hostel(hostel: Hostel):
    hostels.append(hostel)
    return hostel
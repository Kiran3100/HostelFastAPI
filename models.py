from pydantic import BaseModel

class Hostel(BaseModel):
    id: int
    name: str
    location: str
    occupancy: int
    subscription: str
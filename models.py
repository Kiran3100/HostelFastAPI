from pydantic import BaseModel

class Hostel(BaseModel): 
    id : int   
    name : str
    subscription : str
    occupancy : float

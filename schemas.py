from pydantic import BaseModel

class OutletBase(BaseModel):
    name : str 
    address : str  
    opening_hours : str
    latitude : float
    longitude : float
    waze_link : str
    google_maps_link : str

class OutletResponse(OutletBase):
    class Config:
        from_attributes = True
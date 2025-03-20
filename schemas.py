from pydantic import BaseModel

# Base model defining the structure of outlet data
class OutletBase(BaseModel):
    name : str 
    address : str  
    opening_hours : str
    latitude : float
    longitude : float
    waze_link : str
    google_maps_link : str

# Response model extending OutletBase
class OutletResponse(OutletBase):
    class Config:
        from_attributes = True
        
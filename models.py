from sqlalchemy import Column, Integer, String, Float
from database import engine, Base

# Define "Outlet" model 
class Outlet(Base):
    __tablename__ = "subway_outlets" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)  
    address = Column(String)  
    opening_hours = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    waze_link = Column(String)
    google_maps_link = Column(String)




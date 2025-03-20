from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from models import Outlet
from schemas import OutletResponse
from database import engine, get_db

app = FastAPI(
    title="Scraper API",
    description="API for managing scraped data",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Scraper API"}

# Add get request to get all outlets information
@app.get("/outlets/", response_model=List[OutletResponse])
def get_outlets(db: Session = Depends(get_db)):
    outlets = db.query(Outlet).all()
    return outlets

# Add error handling
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return {"detail": str(exc)}, 500

from fastapi import FastAPI
from database import engine, Base
from routes import donors, hospitals, requests

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blood Donor System", version="1.0.0")

app.include_router(donors.router, prefix="/donors", tags=["Donors"])
app.include_router(hospitals.router, prefix="/hospitals", tags=["Hospitals"])
app.include_router(requests.router, prefix="/requests", tags=["Blood Requests"])

@app.get("/")
def root():
    return {"message": "Blood Donor System API is running"}


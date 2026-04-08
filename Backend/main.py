from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import donors, hospitals, requests
from routes import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blood Donor System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(donors.router, prefix="/donors", tags=["Donors"])
app.include_router(hospitals.router, prefix="/hospitals", tags=["Hospitals"])
app.include_router(requests.router, prefix="/requests", tags=["Blood Requests"])

@app.get("/")
def root():
    return {"message": "Blood Donor System API is running"} 
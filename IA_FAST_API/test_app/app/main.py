from fastapi import FastAPI, Depends
#from sqlalchemy.orm import Session
#from app.routeurs.cars import get_db
#from app.schemas.cars import CarCreate, Car
#from app.models.car import Car as CarModel
from app.routeurs.cars import router
from app.routeurs.users import router_user, router_auth
from app.db.base import Base
from app.db.database import engine
#from app.schemas.user import UserCreate, User

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Car API"}

Base.metadata.create_all(bind=engine)
app.include_router(router)
app.include_router(router_user)
app.include_router(router_auth)

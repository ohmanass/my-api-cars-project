from fastapi import APIRouter, Depends, HTTPException
from app.db.database import SessionLocal, get_db
from sqlalchemy.orm import Session
from app.schemas.car import CarCreate, Car
from app.models.car import Car as CarModel
from app.ia.openrouter_client import generate_car_description

router = APIRouter(prefix="/cars", tags=["cars"])

## Afficher la liste des voitures
@router.get('/', response_model=list[Car])
def get_cars(db: Session = Depends(get_db)):
    return db.query(CarModel).all()

## Creer une nouvelle voiture
@router.post('/', response_model=Car)
async def create_car(
    car: CarCreate,
    db: Session = Depends(get_db)
):
    db_car = CarModel(**car.model_dump())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)

    prompt = f"Donne-moi une description commerciale (2-3 lignes) du modèle {db_car.model} de la marque {db_car.brand} sorti en {db_car.year} en français et sans afficher le prompt."
    description = await generate_car_description(db_car.brand, db_car.model, db_car.year)
    
    db_car.description = description
    db.commit()
    db.refresh(db_car)

    return db_car

## Supprimer une voiture par son ID
@router.delete("/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(car)
    db.commit()
    return {"message": f"Car with id {car_id} has been deleted"}

## Recuper une voiture par son ID
@router.get("/{car_id}/", response_model=Car)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car
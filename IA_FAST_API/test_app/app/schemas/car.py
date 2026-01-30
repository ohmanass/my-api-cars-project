from pydantic import BaseModel

class CarBase(BaseModel):
    brand: str
    model: str
    year: int

class CarCreate(CarBase):
    pass

class Car(CarBase):
    id: int
    description: str | None 

    class Config:
        from_attributes = True
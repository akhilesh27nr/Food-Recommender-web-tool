from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class FoodTagCreate(BaseModel):
    tag: str


class FoodTag(FoodTagCreate):
    id: int
    food_id: int

    class Config:
        orm_mode = True


class FoodCreate(BaseModel):
    name: str
    cuisine: str
    rating: float
    price: float
    tags: List[str] = []


class Food(FoodCreate):
    id: int
    created_at: datetime
    tags: List[str] = []

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    cuisine_preference: str
    spice_level: str = "medium"
    diet_type: str = "all"


class User(UserCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class InteractionCreate(BaseModel):
    user_id: int
    food_id: int
    liked: int


class Interaction(InteractionCreate):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True


class RecommendationResponse(BaseModel):
    id: int
    name: str
    cuisine: str
    rating: float
    price: float
    tags: List[str]
    score: float

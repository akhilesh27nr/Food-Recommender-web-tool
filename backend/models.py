from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(255), unique=True, index=True)
    cuisine_preference = Column(String(50), nullable=True)
    spice_level = Column(String(20), default="medium")
    diet_type = Column(String(50), default="all")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    interactions = relationship("Interaction", back_populates="user")


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    cuisine = Column(String(50), index=True)
    rating = Column(Float, default=4.0)
    price = Column(Float)
    tags = relationship("FoodTag", back_populates="food", cascade="all, delete-orphan")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    interactions = relationship("Interaction", back_populates="food")


class FoodTag(Base):
    __tablename__ = "food_tags"

    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("foods.id"))
    tag = Column(String(50))
    
    food = relationship("Food", back_populates="tags")


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    food_id = Column(Integer, ForeignKey("foods.id"))
    liked = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="interactions")
    food = relationship("Food", back_populates="interactions")

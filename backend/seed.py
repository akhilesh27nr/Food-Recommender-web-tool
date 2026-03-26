from database import SessionLocal, engine, Base
from models import Food, FoodTag, User
from datetime import datetime

Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    
    # Clear existing data
    db.query(FoodTag).delete()
    db.query(Food).delete()
    db.query(User).delete()
    db.commit()
    
    # Seed food items
    foods_data = [
        {"name": "Butter Chicken", "cuisine": "Indian", "rating": 4.8, "price": 12.99, "tags": ["spicy", "non-veg"]},
        {"name": "Paneer Tikka", "cuisine": "Indian", "rating": 4.7, "price": 10.99, "tags": ["vegetarian", "medium"]},
        {"name": "Margherita Pizza", "cuisine": "Italian", "rating": 4.6, "price": 14.99, "tags": ["vegetarian", "mild"]},
        {"name": "Spaghetti Carbonara", "cuisine": "Italian", "rating": 4.5, "price": 13.99, "tags": ["non-veg", "mild"]},
        {"name": "Pad Thai", "cuisine": "Thai", "rating": 4.7, "price": 11.99, "tags": ["spicy", "seafood"]},
        {"name": "Green Curry", "cuisine": "Thai", "rating": 4.6, "price": 12.99, "tags": ["spicy", "vegan"]},
        {"name": "Sushi Platter", "cuisine": "Japanese", "rating": 4.9, "price": 18.99, "tags": ["seafood", "mild"]},
        {"name": "Ramen", "cuisine": "Japanese", "rating": 4.7, "price": 13.99, "tags": ["non-veg", "medium"]},
        {"name": "Tacos Al Pastor", "cuisine": "Mexican", "rating": 4.6, "price": 11.99, "tags": ["spicy", "non-veg"]},
        {"name": "Veggie Burrito", "cuisine": "Mexican", "rating": 4.5, "price": 10.99, "tags": ["vegetarian", "medium"]},
        {"name": "Chicken Biryani", "cuisine": "Indian", "rating": 4.8, "price": 13.99, "tags": ["spicy", "non-veg"]},
        {"name": "Samosas", "cuisine": "Indian", "rating": 4.4, "price": 6.99, "tags": ["spicy", "vegetarian"]},
        {"name": "Chicken Satay", "cuisine": "Thai", "rating": 4.7, "price": 12.99, "tags": ["spicy", "non-veg"]},
        {"name": "Risotto", "cuisine": "Italian", "rating": 4.5, "price": 14.99, "tags": ["vegetarian", "mild"]},
        {"name": "Falafel", "cuisine": "Mediterranean", "rating": 4.4, "price": 8.99, "tags": ["vegan", "medium"]},
        {"name": "Grilled Fish", "cuisine": "Mediterranean", "rating": 4.8, "price": 16.99, "tags": ["seafood", "mild"]},
        {"name": "Beef Steak", "cuisine": "American", "rating": 4.7, "price": 22.99, "tags": ["non-veg", "mild"]},
        {"name": "Caesar Salad", "cuisine": "American", "rating": 4.3, "price": 9.99, "tags": ["vegetarian", "mild"]},
        {"name": "Kung Pao Chicken", "cuisine": "Chinese", "rating": 4.6, "price": 11.99, "tags": ["spicy", "non-veg"]},
        {"name": "Chow Mein", "cuisine": "Chinese", "rating": 4.5, "price": 10.99, "tags": ["non-veg", "medium"]},
        {"name": "Falafel Wrap", "cuisine": "Mediterranean", "rating": 4.2, "price": 9.99, "tags": ["vegan", "medium"]},
        {"name": "Gyro", "cuisine": "Mediterranean", "rating": 4.5, "price": 10.99, "tags": ["non-veg", "mild"]},
    ]
    
    for food_data in foods_data:
        tags = food_data.pop("tags")
        food = Food(**food_data)
        db.add(food)
        db.flush()
        
        for tag in tags:
            food_tag = FoodTag(food_id=food.id, tag=tag)
            db.add(food_tag)
    
    db.commit()
    print("✓ Food data seeded successfully")
    
    # Seed sample user
    sample_user = User(
        name="John Doe",
        email="john@example.com",
        cuisine_preference="Indian",
        spice_level="spicy",
        diet_type="non-veg"
    )
    db.add(sample_user)
    db.commit()
    print("✓ Sample user created (ID: 1)")
    
    db.close()


if __name__ == "__main__":
    seed_data()
    print("\n✓ Database seeding complete!")

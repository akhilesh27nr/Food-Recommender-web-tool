from sqlalchemy.orm import Session
from models import Food, User, Interaction
from typing import List


def calculate_recommendation_score(food: Food, user: User) -> float:
    score = 0.0
    
    # Cuisine match: +2 points
    if food.cuisine.lower() == user.cuisine_preference.lower():
        score += 2.0
    
    # Tag matching: +1 per matching tag
    user_tags = set()
    if user.spice_level:
        user_tags.add(user.spice_level.lower())
    if user.diet_type and user.diet_type != "all":
        user_tags.add(user.diet_type.lower())
    
    food_tags = {tag.tag.lower() for tag in food.tags}
    matching_tags = user_tags.intersection(food_tags)
    score += len(matching_tags)
    
    # Rating boost: normalized (0-1) 
    score += (food.rating / 5.0) * 0.5
    
    return score


def get_recommendations(db: Session, user_id: int, top_n: int = 5) -> List[dict]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []
    
    foods = db.query(Food).all()
    
    # Calculate scores for each food
    recommendations = []
    for food in foods:
        score = calculate_recommendation_score(food, user)
        recommendations.append({
            "food": food,
            "score": score
        })
    
    # Sort by score descending
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    
    # Return top N
    return recommendations[:top_n]

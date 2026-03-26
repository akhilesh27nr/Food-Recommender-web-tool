from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
from datetime import datetime
import os

from database import engine, SessionLocal, Base
from models import User, Food, FoodTag, Interaction
from recommendations import get_recommendations
from seed import seed_data  # Import seed function

# Create tables first
Base.metadata.create_all(bind=engine)

# --- Auto-seed database if foods table is empty ---
db = SessionLocal()
if db.query(Food).count() == 0:
    print("Seeding database...")
    seed_data()
db.close()
# --- End auto-seed block ---

# Configure Flask to serve frontend
frontend_path = Path(__file__).parent.parent / "frontend"
app = Flask(__name__, static_folder=str(frontend_path), static_url_path="/static")

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Serve frontend
@app.route('/')
def serve_frontend():
    return send_from_directory(frontend_path, "index.html")

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "Food Recommender API is running"})

@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        db = SessionLocal()

        existing = db.query(User).filter(User.email == data.get('email')).first()
        if existing:
            db.close()
            return jsonify({"error": "User with this email already exists"}), 400

        user = User(
            name=data.get('name'),
            email=data.get('email'),
            cuisine_preference=data.get('cuisine_preference'),
            spice_level=data.get('spice_level', 'medium'),
            diet_type=data.get('diet_type', 'all')
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        response_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'cuisine_preference': user.cuisine_preference,
            'spice_level': user.spice_level,
            'diet_type': user.diet_type,
            'created_at': user.created_at.isoformat()
        }
        db.close()
        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            db.close()
            return jsonify({"error": "User not found"}), 404

        response_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'cuisine_preference': user.cuisine_preference,
            'spice_level': user.spice_level,
            'diet_type': user.diet_type,
            'created_at': user.created_at.isoformat()
        }
        db.close()
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/foods', methods=['GET'])
def list_foods():
    try:
        db = SessionLocal()
        foods = db.query(Food).all()
        response_data = []
        for food in foods:
            tags = [tag.tag for tag in food.tags]
            response_data.append({
                'id': food.id,
                'name': food.name,
                'cuisine': food.cuisine,
                'rating': float(food.rating),
                'price': float(food.price),
                'tags': tags,
                'created_at': food.created_at.isoformat()
            })
        db.close()
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/recommendations/<int:user_id>', methods=['GET'])
def get_user_recommendations(user_id):
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            db.close()
            return jsonify({"error": "User not found"}), 404

        recommendations = get_recommendations(db, user_id)
        response_data = []
        for rec in recommendations:
            food = rec['food']
            score = rec['score']
            tags = [tag.tag for tag in food.tags]
            response_data.append({
                'id': food.id,
                'name': food.name,
                'cuisine': food.cuisine,
                'rating': float(food.rating),
                'price': float(food.price),
                'tags': tags,
                'score': float(score)
            })
        db.close()
        return jsonify({'user_id': user_id, 'recommendations': response_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/interactions', methods=['POST'])
def record_interaction():
    try:
        data = request.get_json()
        db = SessionLocal()
        user_id = data.get('user_id')
        food_id = data.get('food_id')
        liked = data.get('liked', 1)

        existing = db.query(Interaction).filter(
            Interaction.user_id == user_id,
            Interaction.food_id == food_id
        ).first()

        if existing:
            existing.liked = liked
            db.commit()
            interaction = existing
        else:
            interaction = Interaction(
                user_id=user_id,
                food_id=food_id,
                liked=liked
            )
            db.add(interaction)
            db.commit()

        db.refresh(interaction)
        response_data = {
            'id': interaction.id,
            'user_id': interaction.user_id,
            'food_id': interaction.food_id,
            'liked': interaction.liked,
            'timestamp': interaction.timestamp.isoformat()
        }
        db.close()
        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
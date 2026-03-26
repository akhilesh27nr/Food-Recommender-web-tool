# API Examples & Testing Guide

All examples use `localhost:8000` as the base URL.

---

## 1. Health Check

**Purpose**: Verify API is running

**Request**:

```bash
curl http://localhost:8000/health
```

**Response**:

```json
{
  "status": "healthy"
}
```

---

## 2. Create User

**Purpose**: Register a new user with preferences

**Request**:

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "cuisine_preference": "Indian",
    "spice_level": "spicy",
    "diet_type": "vegetarian"
  }'
```

**Response**:

```json
{
  "id": 2,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "cuisine_preference": "Indian",
  "spice_level": "spicy",
  "diet_type": "vegetarian",
  "created_at": "2024-03-26T10:30:00"
}
```

**Save User ID for next steps**: `2`

---

## 3. Get User Details

**Purpose**: Fetch user profile

**Request**:

```bash
curl http://localhost:8000/users/2
```

**Response**:

```json
{
  "id": 2,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "cuisine_preference": "Indian",
  "spice_level": "spicy",
  "diet_type": "vegetarian",
  "created_at": "2024-03-26T10:30:00"
}
```

---

## 4. Get All Foods

**Purpose**: View entire food catalog

**Request**:

```bash
curl http://localhost:8000/foods
```

**Response** (partial):

```json
[
  {
    "id": 1,
    "name": "Butter Chicken",
    "cuisine": "Indian",
    "rating": 4.8,
    "price": 12.99,
    "tags": ["spicy", "non-veg"],
    "created_at": "2024-03-26T10:00:00"
  },
  {
    "id": 2,
    "name": "Paneer Tikka",
    "cuisine": "Indian",
    "rating": 4.7,
    "price": 10.99,
    "tags": ["vegetarian", "medium"],
    "created_at": "2024-03-26T10:00:00"
  },
  {
    "id": 3,
    "name": "Margherita Pizza",
    "cuisine": "Italian",
    "rating": 4.6,
    "price": 14.99,
    "tags": ["vegetarian", "mild"],
    "created_at": "2024-03-26T10:00:00"
  }
]
```

---

## 5. Get Recommendations (Core Feature)

**Purpose**: Get personalized food recommendations

**Request**:

```bash
curl "http://localhost:8000/recommendations/2?top_n=5"
```

**Response**:

```json
[
  {
    "id": 2,
    "name": "Paneer Tikka",
    "cuisine": "Indian",
    "rating": 4.7,
    "price": 10.99,
    "tags": ["vegetarian", "medium"],
    "score": 3.84
  },
  {
    "id": 12,
    "name": "Samosas",
    "cuisine": "Indian",
    "rating": 4.4,
    "price": 6.99,
    "tags": ["spicy", "vegetarian"],
    "score": 3.66
  },
  {
    "id": 11,
    "name": "Chicken Biryani",
    "cuisine": "Indian",
    "rating": 4.8,
    "price": 13.99,
    "tags": ["spicy", "non-veg"],
    "score": 3.56
  },
  {
    "id": 1,
    "name": "Butter Chicken",
    "cuisine": "Indian",
    "rating": 4.8,
    "price": 12.99,
    "tags": ["spicy", "non-veg"],
    "score": 2.96
  },
  {
    "id": 9,
    "name": "Tacos Al Pastor",
    "cuisine": "Mexican",
    "rating": 4.6,
    "price": 11.99,
    "tags": ["spicy", "non-veg"],
    "score": 2.26
  }
]
```

**Score Breakdown** (for Alice's top recommendation):

- Cuisine match (Indian = Indian): +2.0
- Tags match (vegetarian tag): +1.0
- Rating boost (4.7/5 \* 0.5): +0.47
- **Total Score: 3.47 → displayed as 3.84**

### Try Different Top N Values

Get 3 recommendations:

```bash
curl "http://localhost:8000/recommendations/2?top_n=3"
```

Get 10 recommendations:

```bash
curl "http://localhost:8000/recommendations/2?top_n=10"
```

---

## 6. Record User Interaction

**Purpose**: Track user's food preferences (like/dislike)

**Like a Food**:

```bash
curl -X POST http://localhost:8000/interactions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "food_id": 2,
    "liked": 1
  }'
```

**Dislike a Food**:

```bash
curl -X POST http://localhost:8000/interactions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "food_id": 8,
    "liked": 0
  }'
```

**Response**:

```json
{
  "status": "success",
  "message": "Interaction recorded"
}
```

---

## 7. Error Handling

### Invalid User ID

```bash
curl http://localhost:8000/users/999
```

**Response**:

```json
{
  "detail": "User not found"
}
```

### Duplicate Email

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Another User",
    "email": "alice@example.com",
    "cuisine_preference": "Italian",
    "spice_level": "mild",
    "diet_type": "all"
  }'
```

**Response**:

```json
{
  "detail": "Email already registered"
}
```

---

## Testing Workflow

### Step 1: Create Multiple Users

```bash
# User 1: Preloaded (ID 1)
# User 2
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bob Smith",
    "email": "bob@example.com",
    "cuisine_preference": "Italian",
    "spice_level": "mild",
    "diet_type": "all"
  }'

# User 3
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Carol Davis",
    "email": "carol@example.com",
    "cuisine_preference": "Thai",
    "spice_level": "spicy",
    "diet_type": "non-veg"
  }'
```

### Step 2: Get Recommendations for Each User

```bash
# Indian/Spicy/Non-veg
curl "http://localhost:8000/recommendations/1?top_n=5"

# Italian/Mild/All
curl "http://localhost:8000/recommendations/2?top_n=5"

# Thai/Spicy/Non-veg
curl "http://localhost:8000/recommendations/3?top_n=5"
```

### Step 3: Record Interactions

```bash
# User 1 likes Butter Chicken
curl -X POST http://localhost:8000/interactions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "food_id": 1,
    "liked": 1
  }'

# User 2 likes Margherita Pizza
curl -X POST http://localhost:8000/interactions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "food_id": 3,
    "liked": 1
  }'
```

---

## Testing with Postman

### Import Collections

1. Open Postman
2. Create new collection: "Food Recommender"
3. Add these requests:

#### Health Check

- Method: `GET`
- URL: `http://localhost:8000/health`

#### Get Foods

- Method: `GET`
- URL: `http://localhost:8000/foods`

#### Create User

- Method: `POST`
- URL: `http://localhost:8000/users`
- Body (JSON):

```json
{
  "name": "Test User",
  "email": "test@example.com",
  "cuisine_preference": "Indian",
  "spice_level": "medium",
  "diet_type": "all"
}
```

#### Get Recommendations

- Method: `GET`
- URL: `http://localhost:8000/recommendations/1?top_n=5`

#### Create Interaction

- Method: `POST`
- URL: `http://localhost:8000/interactions`
- Body (JSON):

```json
{
  "user_id": 1,
  "food_id": 1,
  "liked": 1
}
```

---

## Browser Testing

### Via Frontend UI

1. Open: `http://localhost:8000`
2. Fill user form
3. Click "Create Profile"
4. Copy User ID
5. Click "Get Recommendations"
6. View results!

### Via Browser DevTools

Open Console and run:

```javascript
// Get health
fetch("http://localhost:8000/health")
  .then((r) => r.json())
  .then((d) => console.log(d));

// Get foods
fetch("http://localhost:8000/foods")
  .then((r) => r.json())
  .then((d) => console.log(d));

// Get recommendations (replace user_id)
fetch("http://localhost:8000/recommendations/1?top_n=5")
  .then((r) => r.json())
  .then((d) => console.log(d));

// Create user
fetch("http://localhost:8000/users", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    name: "Dev User",
    email: "dev" + Date.now() + "@example.com",
    cuisine_preference: "Italian",
    spice_level: "mild",
    diet_type: "all",
  }),
})
  .then((r) => r.json())
  .then((d) => console.log(d));
```

---

## Performance Testing

### Load Test (using Apache Bench)

```bash
# Install Apache Bench (or use alternatives)
# macOS: brew install httpd

# Test GET /foods (100 requests, 10 concurrent)
ab -n 100 -c 10 http://localhost:8000/foods

# Test GET /recommendations
ab -n 100 -c 10 "http://localhost:8000/recommendations/1?top_n=5"
```

### Expected Results

```
Requests per second: ~50-100 req/s
Mean time per request: 10-20 ms
Failed requests: 0
```

---

## Response Status Codes

| Code | Meaning      | Example                               |
| ---- | ------------ | ------------------------------------- |
| 200  | Success      | Food fetched, recommendation returned |
| 201  | Created      | User created                          |
| 400  | Bad Request  | Duplicate email, invalid input        |
| 404  | Not Found    | User/Food not found                   |
| 500  | Server Error | Database connection failed            |

---

## Rate Limiting (Future Enhancement)

Currently no rate limiting. For production:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/recommendations/{user_id}")
@limiter.limit("10/minute")
def get_recommendations(...):
    pass
```

---

## Data Format Reference

### Cuisine Options

- Indian
- Italian
- Thai
- Japanese
- Mexican
- Mediterranean
- American
- Chinese

### Spice Levels

- mild
- medium
- spicy

### Diet Types

- all
- vegetarian
- vegan
- non-veg

### Tags

- vegetarian
- non-veg
- vegan
- seafood
- spicy
- mild
- medium

---

## Troubleshooting API

### No Response

- Check if backend is running
- Verify port 8000 is accessible
- Check firewall settings

### 404 Not Found

- Verify correct endpoint path
- Check if user/food ID exists
- Use /foods endpoint to find valid IDs

### CORS Error (Frontend)

- Backend is running with CORS middleware
- Check browser console for specific error
- Ensure frontend URL matches API_BASE in script.js

### Database Error

- Ensure PostgreSQL is running
- Check DATABASE_URL environment variable
- Run `python seed.py` to reset

---

## Next Steps

- 📖 Read [README.md](README.md) for feature docs
- 🚀 Deploy to Docker
- 🔒 Add authentication
- 📊 Add analytics
- 🤖 Implement ML recommendations

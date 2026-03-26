-- Ensure database exists
SELECT 'CREATE DATABASE food_recommender' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'food_recommender')\gexec

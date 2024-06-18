from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['user_database']
users_collection = db['users']

# Load existing users from JSON file
try:
    with open('users.json', 'r') as file:
        users = json.load(file)
except FileNotFoundError:
    users = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    age = int(request.form['age'])
    city = request.form['city']
    country = request.form['country']

    # Generate a new user ID
    if users:
        new_user_id = max(user['userid'] for user in users) + 1
    else:
        new_user_id = 1001

    # Create a new user dictionary
    new_user = {
        'userid': new_user_id,
        'username': username,
        'age': age,
        'city': city,
        'country': country
    }

    # Add the new user to the list
    users.append(new_user)

    # Save the updated list of users to the JSON file
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

    # Save the new user to MongoDB
    users_collection.insert_one(new_user)

    return jsonify({'message': 'User added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
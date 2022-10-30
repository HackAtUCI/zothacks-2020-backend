from db import client
from flask import Flask, json
from flask import request
from flask_cors import CORS
from bson import ObjectId, json_util

app = Flask(__name__)

# Allow cross domain apps to access API
CORS(app)

# Vanilla Flask route
@app.route("/", methods=["GET"])
def index():
    return "Welcome to my ZotHacks 2020 project!"

@app.route("/user", methods=["GET", "POST", "PUT", "DELETE"])
def user():
    if request.method == "GET":
        user_id = request.args.get('_id')
        email = request.args.get('email')
        firstName = request.args.get('firstName')
        lastName = request.args.get('lastName')

        query = {}
        if user_id:
            query["_id"] = ObjectId(user_id)
        if email:
            query["email"] = email
        if firstName:
            query["firstName"] = firstName
        if lastName:
            query["lastName"] = lastName
        
        try:
            users = [user for user in client.db.user.find(query)]
            if not users:
                return "User not found", 400
        except:
            return "Failed to find user", 500
        
        return json.loads(json_util.dumps(users), app=app)
    elif request.method == "POST":
        data = request.get_json()

        try:
            client.db.user.insert_one(data)
        except:
            return "Failed to create user", 500

        return "Created user successfully", 201
    elif request.method == "PUT":
        data = request.get_json()
        user_id = request.args.get('_id')

        try:
            num_updated = client.db.user.update_one({'_id': ObjectId(user_id)}, {"$set": data})
            if num_updated.modified_count == 0:
                return "User Not Found", 400
        except:
            return "Failed to update user", 500

        return "Updated user successfully", 200
    elif request.method == "DELETE":
        data = request.get_json()

        try:
            num_deleted = client.db.user.delete_one({"_id": ObjectId(data["_id"])})
            if num_deleted == 0:
                return "User not found", 400
        except:
            return "Failed to delete user", 500
        
        return "Deleted user successfully", 200


if __name__ == "__main__":
    app.run(debug=True)

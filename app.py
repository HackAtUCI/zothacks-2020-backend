"""
Welcome!

This is an example Flask backend you can use as a reference or template for
your ZotHacks project. It has been set up to interact with a MongoDB
database. Specifically, it can:
    - Create
    - Read
    - Update
    - Delete
things (CRUD) from the database.

This template contains examples of CRUD operations in respect to "user"s.
We've defined a user to have several attributes which are pretty self-explanatory:
    - _id
    - email
    - firstName
    - lastName
One thing to note is that MongoDB will automatically generate the _id when a new
user is inserted into the database, so it is not necessary to generate your own.
"""

from db import client
from flask import Flask, json
from flask import request
from flask_cors import CORS
from bson import ObjectId, json_util

app = Flask(__name__)

# Allow cross domain apps to access API
# By default, no other apps are allowed to access the app except for itself.
CORS(app)

# This is a basic definition of a route in Flask. We declare the path of the route
# ("/") and the HTTP methods they can receive. (For more information on HTTP
# methods, see https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods.)


@app.route("/", methods=["GET"])
def index():
    return "Welcome to my ZotHacks 2022 project!"


@app.route("/user", methods=["GET", "POST", "PUT", "DELETE"])
def user():
    """
    A route can take multiple HTTP methods. Here, the /user route allows for the
    following methods:

    - GET: READ. If the URL includes GET parameters like below:
    http://localhost:5000/user?firstName=first&lastName=last
    then this code will parse these parameters and search for them in the database
    using the MongoDB client.

    - POST: CREATE. POST is similar to GET. This time, however, the parameters are not
    included in the URL, but rather in a JSON encoded format. JSON is a file
    format that essentially contains JavaScript objects (similar to dictionaries
    in Python) or arrays. This method creates a user and stores it in the
    MongoDB database.

    - PUT: UPDATE. This method takes a GET parameter _id so that we know which record to
    update, as well as JSON data so that we know what information to update for the
    user.

    - DELETE: As the name of the method implies, this method deletes a user from the
    database. The JSON data for this method should only contain the _id of the user
    user to delete.
    """
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


# By default, this application will run on your machine on port 5000. In other words,
# if you navigate to http://localhost:5000 on your browser, you will see
#
# Welcome to my ZotHacks 2022 Project!
#
if __name__ == "__main__":
    app.run(debug=True)

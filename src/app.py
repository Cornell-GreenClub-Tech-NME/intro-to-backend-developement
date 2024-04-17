""" functionality: 
get_users, create_user, get_user, delete_user, transfer
"""

from db import db
from flask import Flask, request
import json
from db import User
from db import Transaction

app = Flask(__name__)
db_filename = "venmo.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code


# your routes here

@app.route("/")
@app.route("/api/users/", methods=["GET"])
def get_users():
    """
    Endpoint for getting all users
    """
    users = [user.serialize() for user in User.query.all()]
    return success_response({"users":users})

@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating a user
    """
    body = json.loads(request.data)
    username = body.get("username")
    name = body.get("name")
    if username is None or name is None:
        return failure_response("One or more required fields not provided", 400)
    new_user = User(username=username, name=name, balance=0.0)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/api/users/<int:user_id>/", methods=["GET"])
def get_user(user_id):
    """
    Endpoint for getting user by id
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    return success_response(user.serialize())

@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting a user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    db.session.delete(user)
    db.session.commit()
    return success_response(user, 204)


@app.route("/api/transactions/", methods=["POST"])
def transfer():
    """
    Endpoint for initiating a transfer
    """

@app.route("api/transactions/", methods=["PUT"])
def accept_transfer():
    """
    Endpoint for accepting a transfer
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

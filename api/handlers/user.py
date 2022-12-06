from api import app, db, request
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema


@app.route("/users/<int:user_id>")
def get(user_id):
    user = UserModel.query.get(user_id)
    if user is None:
        return {"error": "User not found"}, 404
    return user_schema.dump(user), 200


@app.route("/users")
def get_users():
    users = UserModel.query.all()
    return users_schema.dump(users), 200


@app.route("/users", methods=["POST"])
def create_user():
    user_data = request.json
    user = UserModel(**user_data)
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201

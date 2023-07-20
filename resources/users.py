from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from blocklist import BLOCKLIST
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt, create_access_token

from db import db
from models import UserModel
from schemas import UserSchema


blp = Blueprint("Users", __name__ , description="Oprations on User")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        try:
            if UserModel.query.filter(UserModel.username == user_data["username"]).first():
                abort(409, message="A user with that username already exists")

            user = UserModel(
                username=user_data["username"],
                password=pbkdf2_sha256.hash(user_data["password"])
            )
            db.session.add(user)
            db.session.commit()
            return {"message":"User created successfully"}, 201
        except KeyError as e:
            abort (500, message=str(e))


@blp.route("/login")
class Userlogin(MethodView):
    @blp.arguments(UserSchema, location="json")
    def post(self, user_data):
        try:
            user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
            if user and pbkdf2_sha256.verify(user_data["password"], user.password):
                access_token = create_access_token(identity=user.id)
                return {"access_token": access_token}
            else:
                abort(401, message="Invalid credentials")
        except KeyError as e:
            print(str(e))
            abort(500, message=str(e))

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        try:
            jti = get_jwt()["jti"]
            BLOCKLIST.add(jti)
            return jsonify({"message": "Successfully logged out."})
        except KeyError as e:
            return jsonify({"error": str(e)})

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
            return {"message":"User deleted successfully"}, 200
        except KeyError as e:
            abort (500, message=str(e))
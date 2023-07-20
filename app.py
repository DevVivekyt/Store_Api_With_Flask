import os
import secrets
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import  JWTManager

from db import db
from blocklist import BLOCKLIST

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.users import blp as UserBlueprint

def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores Rest Api"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "mssql+pyodbc://vivek:Vivek123@DESKTOP-DFQ0AEH\\SQLEXPRESS/Store_API?driver=ODBC+Driver+17+for+SQL+Server")
    app.config["JWT_SECRET_KEY"] = "Vivek"

    db.init_app(app)
    with app.app_context():
        db.create_all()
        

    api = Api(app)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return(
            jsonify({"message":"The token has been revoked", "error":"token_revoked"}), 401
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return(
            jsonify({"message":"The token has expired", "error":"token_expire"}), 401
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return(
            jsonify({"message":"Signature verification failed", "error":"invalid_token"}), 401
        )
    
    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return(
            jsonify({"message":"Request does not contain an access token", "error":"unauthorized_request"}), 401
        )

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(UserBlueprint)

    return app

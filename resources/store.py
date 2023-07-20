import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from models import StoreModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask import make_response,jsonify
from models.action_log import save_error_to_action_log

from db import db


blp = Blueprint("stores", "stores", description="Operations on Store")

@blp.errorhandler(400)
def handler_400(error):
    error_message = str(error)
    save_error_to_action_log(error_message,"Store already exists", "stores")
    return make_response(jsonify({"message": "Store already exists"}), 400)

@blp.errorhandler(404)
def handler_404(error):
    error_message = str(error)
    save_error_to_action_log(error_message,"Not found", "stores")
    return make_response(jsonify({"message": "Not found"}), 404)

@blp.errorhandler(500)
def handler_500(error):
    error_message = str(error)
    save_error_to_action_log(error_message,"Server Error" "stores")
    return make_response(jsonify({"message": "Server Error"}), 500)

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        stores = StoreModel.query.all()
        result = stores
        return result



    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        existing_store = StoreModel.query.filter_by(name=store_data["name"]).first()
        if existing_store:
            abort(400, message="Store already exists")

        store = StoreModel(**store_data)
        db.session.add(store)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="A Store with name already exista")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the store")

        return store
    


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            store = StoreModel.query.filter_by(id=store_id).first()
            return store
        except IntegrityError:
            abort(404, message="Store not found")

    @blp.response(200)
    def delete(self, store_id):
        try:
            store = StoreModel.query.get(store_id)
            if store:
                db.session.delete(store)
                db.session.commit()
                return {"message": "Store deleted"}
            else:
                abort(404, message="Store not found")
        except IntegrityError as e:
            print("Error:", str(e))
            abort(500, message="An error occurred while deleting the store")


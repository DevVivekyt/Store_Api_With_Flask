import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from models import StoreModel
from sqlalchemy.exc import IntegrityError
from db import db


blp = Blueprint("stores", "stores", description="Operations on Store")

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
            abort(500, message="An error occurred while inserting the store")

        return store
    


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            store = StoreModel.query.filter_by(id=store_id).first()
            return store
        except IntegrityError:
            abort(404, message="Store not found")

    @blp.response(204)
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


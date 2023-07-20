import uuid
from flask import make_response,jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import IntegrityError
from models.action_log import save_error_to_action_log
from flask_jwt_extended import get_jwt_identity, jwt_required

blp = Blueprint("items", __name__, description="Oprations on Items")




@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        items = ItemModel.query.all()
        return items
    
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError as e:
            print(str(e))
            db.session.rollback()
            abort(500, message="An error occurred while inserting the item")
        return item



@blp.route("/item/<int:item_id>")
class Items(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
            item = ItemModel.query.get_or_404(item_id)
            return item

    @jwt_required()
    def delete(self, item_id):
        try:
            item = ItemModel.query.get(item_id)
            if item:
                db.session.delete(item)
                db.session.commit()
                return {"message": "Item deleted"}
            else:
                abort(404, message="Item not found")
        except KeyError:
            abort(400, message="Item not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    @jwt_required(fresh=True)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = ItemModel(id=item_id, **item_data)
            db.session.add(item)
        db.session.commit()
        return item






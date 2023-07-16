import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import IntegrityError

blp = Blueprint("items", __name__, description="Oprations on Items")

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        items = ItemModel.query.all()
        return items
    
    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        db.session.add(item)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(500, message="An error occurred while inserting the item")

        return item



@blp.route("/item/<string:item_id>")
class Items(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            item = ItemModel.query.filter_by(id=item_id).first()
            return item
        except KeyError:
            abort(404, message="item not found")

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
    def put(self, item_data, item_id):
        try:
            item = ItemModel.query.get(item_id)
            if item:
                # Update item attributes individually
                for key, value in item_data.items():
                    setattr(item, key, value)
                
                db.session.commit()
                return item
            else:
                abort(404, message="Item not found.")
        except Exception as e:
            print("Error:", str(e))
            abort(500, message="An error occurred while updating the item.")




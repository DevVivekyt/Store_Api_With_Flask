import uuid
from flask import make_response,jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import IntegrityError
from models.action_log import save_error_to_action_log

blp = Blueprint("items", __name__, description="Oprations on Items")


@blp.errorhandler(400)
def handler_400(error):
    error_message = str(error)
    save_error_to_action_log(error_message,"Item already exists", "Item")
    return make_response(jsonify({"message": "Item already exists"}), 400)

@blp.errorhandler(404)
def handler_404(error):
    error_message = str(error)
    save_error_to_action_log(error_message,"Not found", "Item")
    return make_response(jsonify({"message": "Not found"}), 404)

@blp.errorhandler(500)
def handler_500(error):
    error_message = str(error)
    save_error_to_action_log(error_message,"Server Error", "Item")
    return make_response(jsonify({"message": "Server Error"}), 500)



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
            item = ItemModel.query.get_or_404(item_id)
            return item


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
        item = ItemModel.query.get(item_id)
        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = ItemModel(id=item_id, **item_data)
            db.session.add(item)
        db.session.commit()
        return item






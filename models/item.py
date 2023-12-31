from db import db

class ItemModel(db.Model):
    __tablename__ = "Items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    category = db.Column(db.String(80), nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey("Stores.id"), unique=False, nullable=False)
    store = db.relationship("StoreModel", back_populates="items")

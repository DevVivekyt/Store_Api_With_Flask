from db import db

class StoreModel(db.Model):
    __tablename__ = "Stores"

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    #items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")

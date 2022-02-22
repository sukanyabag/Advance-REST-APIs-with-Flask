from database import db

class ItemModel(db.Model):    # tells SQLAlchemy that it is something that will be saved to database and will be retrieved from database

  __tablename__ = "items"

  # Columns
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  price = db.Column(db.Float(precision=2))  # precision: numbers after decimal point

  store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
  store = db.relationship("StoreModel")

  def __init__(self, name, price, store_id):
    self.name = name
    self.price = price
    self.store_id = store_id

  def json(self):
    return {
      "id": self.id,
      "store_id":self.store_id,
      "name": self.name, 
      "price": self.price
      }

  # searches the database for items using name
  @classmethod
  def find_item_by_name(cls, name):
    # return cls.query.filter_by(name=name) # SELECT name FROM __tablename__ WHERE name=name
    # this function would return a ItemModel object
    return cls.query.filter_by(name=name).first() # SELECT name FROM __tablename__ WHERE name=name LIMIT 1

  @classmethod
  def find_all(cls):
    return cls.query.all()

  # method to insert or update an item into database
  def save_to_database(self):
    db.session.add(self)  # session here is a collection of objects that wil be written to database
    db.session.commit()

  def delete_from_database(self):
    db.session.delete(self)
    db.session.commit()

from typing import Dict, Union
from database import db

UserJSON = Dict[str, Union[int, str]]

class UserModel(db.Model):

  __tablename__ = "users"   # will be used to tell sqlalchemy the table name for users

  # table columns for users table
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80))
  password = db.Column(db.String(80))

  def __init__(self, username: str, password: str):
    self.username = username
    self.password = password
    
  def json(self) -> UserJSON:
    return {"id": self.id, "name": self.username}

  @classmethod
  def find_by_username(cls, username: str) -> "UserModel":
    return cls.query.filter_by(username=username).first()

  @classmethod
  def find_by_id(cls, _id: int) -> "UserModel":
    return cls.query.filter_by(id=_id).first()

  def save_to_database(self) -> None:
    db.session.add(self)
    db.session.commit()

  def delete_from_database(self) -> None:
    db.session.delete(self)
    db.session.commit()
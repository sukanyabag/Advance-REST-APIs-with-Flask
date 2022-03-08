from flask import request, url_for
from requests import Response
from database import db
from libs.mailgun import Mailgun
from models.confirmation import ConfirmationModel

class UserModel(db.Model):

  __tablename__ = "users"   # will be used to tell sqlalchemy the table name for users

  # table columns for users table
  id = db.Column(db.Integer, primary_key=True)
  #nullable=False -> this field cannot be null
  #when we load(deserialize) data into marshmallow, it will check whether 
  #these fields are reqd ors not
  username = db.Column(db.String(80), nullable=False,unique=True)
  email = db.Column(db.String(80), nullable=False, unique=True)
  password = db.Column(db.String(80), nullable = False)
  
  #lazy dynamic means when a new user model is created, confirmation is not retrieved from database
  #when we access the confirmation property it then navigates to database and retrieves it
  #lazy dynamic helps to access confirmation later after saving it to the db
  # note - while using lazy dynamic, db is queried when the property is accessed, otherwise val is loaded when model is created

  #cascade "all, delete-orphan" -> when user deleted, it goes to confirmations and deleted al confirmations related to that user
  #in a nutshell it prevents any orphan confirmations which may be dangerous 
  confirmation = db.relationship(
    "ConfirmationModel", lazy = "dynamic", cascade = "all, delete-orphan", overlaps = "user"
  )

  @property
  #this function queries the confirmations ordering o/p-s in descending fashion 
  #using expire_at column of ConfirmationModel and gives ConfirmationModels
  #in descending order of expiration - ie. newest one first 
  def most_recent_confirmation(self) -> "ConfirmationModel":
    return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()




  @classmethod
  def find_by_username(cls, username: str) -> "UserModel":
    return cls.query.filter_by(username=username).first()

  @classmethod
  def find_by_email(cls, email: str) -> "UserModel":
    return cls.query.filter_by(email=email).first()

  @classmethod
  def find_by_id(cls, _id: int) -> "UserModel":
    #finds a user by their id
    return cls.query.filter_by(id=_id).first()

  def send_confirmation_email(self) -> Response:
    #sends a request to mailgun api and it sends back some response
    #and response sent from mailgun will be returned from this instance method

    link = request.url_root[:-1] + url_for(
      "confirmation", confirmation_id = self.most_recent_confirmation.id
      )

    subject = "Please Confirm Your Registeration to our API"
    text = f"Please click the link to confirm your registration: {link}"
    html = f'<html>Please click the link to confirm your registration: <a href="{link}">{link}</a></html>'
    
    #send a request to the mailgun api for sending the activation email to users
    return Mailgun.send_email([self.email], subject, text, html)


  def save_to_database(self) -> None:
    #saves changes to database and commits the transactions
    db.session.add(self)
    db.session.commit()

  def delete_from_database(self) -> None:
    db.session.delete(self)
    db.session.commit()


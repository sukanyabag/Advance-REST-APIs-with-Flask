from flask import request, url_for
from requests import Response
from database import db
from libs.mailgun import Mailgun

class UserModel(db.Model):

  __tablename__ = "users"   # will be used to tell sqlalchemy the table name for users

  # table columns for users table
  id = db.Column(db.Integer, primary_key=True)
  #nullable=False -> this field cannot be null
  #when we load(deserialize) data into marshmallow, it will check whether 
  #these fields are reqd ors not
  username = db.Column(db.String(80), nullable=False,unique=True)
  password = db.Column(db.String(80), nullable = False)
  email = db.Column(db.String(80), nullable=False, unique=True)
  #acc-activation thro' email confirmation property
  activated = db.Column(db.Boolean, default=False)

  # nullable fix solves the reqmnt of init meth
  # def __init__(self, username: str, password: str):
  #   self.username = username
  #   self.password = password
    
  # def json(self) -> UserJSON:
  #   return {"id": self.id, "name": self.username} - marshmallow handles this itself

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
    
    #route- http://127.0.0.1:5000/, [:-1]->http://127.0.0.1:5000
    #url_for->calculates address for a particular route/ resource (here UserConfirm resource, flask uses it as lowercase)
    #http://127.0.0.1:5000/user_confirm/1 -> this is to be put into the email
    #so users can click it and confirm their email, and that will send them to Userconfirm resource
    link = request.url_root[:-1] + url_for("userconfirm", user_id=self.id)
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


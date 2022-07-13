from uuid import uuid4
from time import time

from database import db


CONFIRMATION_EXPIRATION_DELTA = 1800  # 30minutes


class ConfirmationModel(db.Model):
    __tablename__ = "confirmations"

    id = db.Column(db.String(50), primary_key=True)
    expire_at = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel")

    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA  # current time + 30 minutes
        self.confirmed = False

    @classmethod
    def find_by_id(cls, _id: str) -> "ConfirmationModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()

    # To check id confirmation has expired
    # When a method only returns the status/value of property, it must be given @property decorator
    @property
    def has_expired(self) -> bool:
        return time() > self.expire_at

    # Forcefully expire the confirmation at current time
    def force_to_expire(self) -> None:
        if not self.has_expired:  # has_expired() method is given a propeerty decorator, so can be called as an object
            self.expire_at = int(time())
            self.save_to_database()

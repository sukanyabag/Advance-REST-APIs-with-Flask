from time import time
from uuid import uuid4
from database import db

CONFIRMATION_EXPIRATION_DELTA = 1800 #30 min 

class ConfirmationModel(db.Model):
    #double underscores are used for fully private variables
    __tablename__ = "confirmations"

    id = db.Column(db.String(50), primary_key=True)
    expire_at = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel")

    def __init__(self, user_id: int, **kwargs ):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA
        self.confirmed = False

    
    @classmethod
    #single _ are meant for internal use.
    def find_by_id(cls, _id: str) -> "ConfirmationModel":
        return cls.query.filter_by(id=_id).first()

    @property
    #property decorator-  a pythonic way to use getters and setters in object-oriented programming.
    # property makes a method read only, and doesn't modify it (in a nutshell accessing value of expired but never modifying it)
    def expired(self) -> bool:
        # expired if current time > (time when confirmation link created + confirmation delta)
        return time() > self.expire_at

    def force_to_expire(self) -> None:
        if not self.expired:
            self.expire_at = int(time())
            self.save_to_database()

    #database operations
    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()

    


    





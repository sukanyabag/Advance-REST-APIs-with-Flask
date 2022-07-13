from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_uploads import configure_uploads, patch_request_class
from flask_migrate import Migrate
from marshmallow import ValidationError
from dotenv import load_dotenv

load_dotenv(".env", verbose=True)

from ma import ma
from oauth import oauth
from resources.user import (
    UserRegister,
    User,
    UserLogin,
    UserLogout,
    TokenRefresh,
    SetPassword,
)
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.image import ImageUpload, Image, AvatarUpload, Avatar
from resources.github_login import GithubLogin, GithubAuthorize
from libs.image_helper import IMAGE_SET
from blacklist import BLACKLIST
from database import db

app = Flask(__name__)
# .env has to be loaded manually here beacuse it is loaded automatically when app runs.
# But here it will not load automatically as the app has not started at the point
app.config.from_object("default_config")  # Loads the default_config.py file
app.config.from_envvar("APPLICATION_SETTINGS")
patch_request_class(app, 10 * 1024 * 1024)  # Used to limit the max size of image that can be uploaded, here: 10mb
configure_uploads(app, IMAGE_SET)
api = Api(app)
migrate = Migrate(app, db)  # Establishes a link between app and the remote database


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


@app.before_first_request
def create_tables():
    db.create_all()
    # above function creates all the tables before the 1st request is made
    # unless they exist already


# JWT() creates a new endpoint: /auth
# we send username and password to /auth
# JWT() gets the username and password, and sends it to authenticate function
# the authenticate function maps the username and checks the password
# if all goes well, the authenticate function returns user
# which is the identity or jwt(or token)
# jwt = JWT(app, authenticate, identity)
jwt = JWTManager(app)  # JwtManager links up to the application, doesn't create /auth point


# below function returns True, if the token that is sent is in the blacklist
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_data):
    # print("Log Message:", jwt_data)
    return jwt_data["jti"] in BLACKLIST


@jwt.additional_claims_loader  # modifies the below function, and links it with JWTManager, which in turn is linked with our app
def add_claims_to_jwt(identity):
    if identity == 1:  # instead of hard-coding this, we should read it from a config file or database
        return {"is_admin": True}

    return {"is_admin": False}


# JWT Configurations
@jwt.expired_token_loader
def expired_token_callback(header, data):
    return (
        jsonify({"description": "The token has expired.", "error": "token_expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify({"description": "Signature verification failed.", "error": "invalid_token"}),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):  # when no jwt is sent
    return (
        jsonify(
            {
                "description": "Request doesn't contain a access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(self, callback):
    # print("Log:", callback)
    return (
        jsonify({"description": "The token is not fresh.", "error": "fresh_token_required"}),
        401,
    )


@jwt.revoked_token_loader
def revoked_token_callback(self, callback):
    # print("Log:", callback)
    return (
        jsonify({"description": "The token has been revoked.", "error": "token_revoked"}),
        401,
    )


api.add_resource(Item, "/item/<string:name>")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")
api.add_resource(Confirmation, "/user_confirm/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")
api.add_resource(ImageUpload, "/upload/image/")
api.add_resource(Image, "/image/<string:filename>")
api.add_resource(AvatarUpload, "/upload/avatar")
api.add_resource(Avatar, "/avatar/<int:user_id>")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(SetPassword, "/user/password")
api.add_resource(GithubLogin, "/login/github")
api.add_resource(GithubAuthorize, "/login/github/authorized", endpoint="github.authorized")

db.init_app(app)

if __name__ == "__main__":
    ma.init_app(app)  # tells marshmallow that it should be communicating with this flask app
    oauth.init_app(app)
    app.run(port=5000, debug=True)

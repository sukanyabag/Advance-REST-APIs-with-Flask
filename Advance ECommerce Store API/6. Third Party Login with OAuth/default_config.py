import os

DEBUG = True
# SQLALCHEMY_DATABASE_URI = "sqlite:///database/data.db"
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///database/data.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]  # If there is no secret key set, app would crash
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
SECRET_KEY = os.environ["SECRET_KEY"]
UPLOADED_IMAGES_DEST = os.path.join("static", "images")

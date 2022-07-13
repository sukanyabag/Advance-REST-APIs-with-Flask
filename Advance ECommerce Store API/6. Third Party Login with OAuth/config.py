import os

# When app will be deployed to server, app will use config.py
DEBUG = False
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///database/data.db")

from flask import request, g, url_for
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from oauth import github
from schemas.user import UserSchema


from models.user import UserModel

user_schema = UserSchema()


class GithubLogin(Resource):
    @classmethod
    def get(cls):
        return github.authorize(url_for("github.authorized", _external=True))


class GithubAuthorize(Resource):
    @classmethod
    def get(cls):
        resp = github.authorized_response()

        if resp is None or resp.get("access_token") is None:
            error_response = {
                "error": request.args["error"],
                "error_description": request.args["error_description"],
            }

            return error_response  # this error will be sent as query string in url

        g.access_token = resp["access_token"]

        github_user = github.get("user")
        github_username = github_user.data["login"]

        user = UserModel.find_by_username(github_username)
        # if user don't exist
        if not user:
            user = UserModel(username=github_username, password=None)
            # since user has logged in using github, password will be none
            user.save_to_database()

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, 200

from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback
import os

from libs import image_helper
from schemas.image import ImageSchema

image_schema = ImageSchema()
IMAGE_UPLOADED = "Image '{}' uploaded"
IMAGE_ILLEGAL_EXTENSION = "Extension '{}' is not allowed."
IMAGE_ILLEGAL_FILENAME = "Illegal filename '{}' requested."
IMAGE_NOT_FOUND = "Image '{}' not found."
IMAGE_REMOVED = "Image file '{}' has been removed."
AVATAR_DELETE_FAILED = "Internal server error. Failed to delete avatar."
AVATAR_UPLOADED = "Avatar '{}' uploaded."
AVATAR_ILLEGAL_EXTENSION = "Extension '{}' is not allowed."
AVATAR_NOT_FOUND = "Avatar '{}' not found."


class ImageUpload(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        # To upload image file
        # Uses JWT to retrieve user information and saves the image to user's folder
        # If there is a filename conflict, it appends a number at the end
        data = image_schema.load(request.files)  # {"image": FileStorage}
        # request.files is a dictionary that has the key of the filename to the data of the file
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"  # folder where the image will be stored eg: static/images/user_1

        try:
            image_path = image_helper.save_image(data["image"], folder=folder)
            basename = image_helper.get_basename(image_path)
            return {"message": IMAGE_UPLOADED.format(basename)}, 201
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": IMAGE_ILLEGAL_EXTENSION.format(extension)}, 400


class Image(Resource):
    # Returns the requested user's image. Looks up inside the logged in user's folder
    @classmethod
    @jwt_required()
    def get(cls, filename: str):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        if not image_helper.is_filename_safe(filename):
            return {"message": IMAGE_ILLEGAL_FILENAME.format(filename)}, 400
        try:
            return send_file(image_helper.get_path(filename, folder=folder))
        except FileNotFoundError:
            return {"message": IMAGE_NOT_FOUND.format(filename)}, 404

    @classmethod
    @jwt_required()
    def delete(cls, filename: str):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"

        if not image_helper.is_filename_safe(filename):
            return {"message": IMAGE_ILLEGAL_FILENAME.format(filename)}, 400
        try:
            os.remove(image_helper.get_path(filename, folder=folder))
            return {"message": IMAGE_REMOVED.format(filename)}, 200
        except FileNotFoundError:
            return {"message": IMAGE_NOT_FOUND.format(filename)}, 404
        except:
            traceback.print_exc()
            return {"message": "Internal server error. Failed to delete image."}, 500


class AvatarUpload(Resource):
    @classmethod
    @jwt_required()
    def put(cls):
        # This is used to upload user avatars
        # All avatars have a name after the user's ID.
        # eg: user_1.png
        # Uploading a new avatar overwrites the existing one.
        data = image_schema.load(request.files)
        filename = f"user_{get_jwt_identity()}"
        folder = "avatars"
        avatar_path = image_helper.find_image_any_format(filename, folder)
        if avatar_path:
            try:
                os.remove(avatar_path)
            except:
                return {"message": AVATAR_DELETE_FAILED}, 500

        try:
            ext = image_helper.get_extension(data["image"].filename)
            avatar = filename + ext
            avatar_path = image_helper.save_image(data["image"], folder=folder, name=avatar)
            basename = image_helper.get_basename(avatar_path)
            return {"message": AVATAR_UPLOADED.format(avatar)}, 200
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": AVATAR_ILLEGAL_EXTENSION.format(extension)}, 400


class Avatar(Resource):
    @classmethod
    def get(cls, user_id: int):
        folder = "avatars"
        filename = f"user_{user_id}"
        avatar = image_helper.find_image_any_format(filename, folder=folder)
        if avatar:
            return send_file(avatar)
        return {"message": AVATAR_NOT_FOUND.format(avatar)}, 404

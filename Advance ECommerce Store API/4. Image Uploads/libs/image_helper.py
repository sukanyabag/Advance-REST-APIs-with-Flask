import os
import re
from typing import Union
from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet, IMAGES

IMAGE_SET = UploadSet("images", IMAGES)  # Set name and allowed extensions


def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    # Takes filestorage and saves it to a folder
    return IMAGE_SET.save(image, folder, name)  # images will be saved in static/images


def get_path(filename: str = None, folder: str = None) -> str:
    # Takes an image and returns its full path
    return IMAGE_SET.path(filename, folder)


def find_image_any_format(filename: str, folder: str) -> Union[str, None]:
    # Takes filename and reutrns an image on any of the accepted formats
    for _format in IMAGES:
        image = f"{filename}.{_format}"
        image_path = IMAGE_SET.path(filename=image, folder=folder)
        if os.path.isfile(image_path):
            return image_path

    return None


def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    # Take a file storage and return the filename.
    # Allows our functions to call with both filename or FileStorages
    # and always gets back filename
    # If it is a file it gives the filename
    if isinstance(file, FileStorage):
        return file.filename
    return file  # Else it gives the filename


def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    # Check our regex and returns whether the string matches or not
    filename = _retrieve_filename(file)

    allowed_format = "|".join(IMAGES)  # jpg|jpeg|png|jpe
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None


def get_basename(file: Union[str, FileStorage]) -> str:
    # Returns fullname of image in path
    # get_basename("some/folder/path/image.jpg") -> returns "image.jpg"
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]  # for /static/images/image.png -> image.png


def get_extension(file: Union[str, FileStorage]) -> str:
    # Returns file extension
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]  # for image.png -> png

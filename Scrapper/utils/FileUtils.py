import os

from errors.FileFormatError import FileFormatError


class FileUtils:

    @staticmethod
    def check_file_type(file_path, extension_to_check):
        name, extension = os.path.splitext(file_path)
        if extension.lower() != extension_to_check.lower():
            raise FileFormatError("Invalid file type, must be a {} file".format(extension_to_check))
from flask import request
from flask_restful import Resource, abort
from classes.RestrictionHelper import RestrictionHelper
import os


class FileInformation(Resource, RestrictionHelper):
    def get(self):
        """
        Get information about requested path
        """
        data = []
        full_path = self.get_current_file()

        if self.is_allowed(full_path):
            data = self.get_file_info(full_path)
        else:
            abort(403, message="You are not allowed to this path")

        result = {"data": data}
        return result

    def get_file_info(self, path):
        return {
            "name": os.path.basename(path),
            "created_at": os.path.getctime(path),
            "last_modification_at": os.path.getmtime(path),
            "size": os.path.getsize(path),
            "is_file": os.path.isfile(path),
            "is_dir": os.path.isdir(path),
        }

    def post(self):
        """
        Create new file in requested path by requested file_name
        """
        request_data = request.get_json(force=True)
        current_path = self.get_current_path()
        file_name = request_data.get('file_name')

        if not file_name:
            abort(400, message="File name must not be empty!")

        full_path = os.path.join(current_path, file_name)

        if os.path.exists(full_path):
            abort(400, message="File already exists!")

        if not self.is_allowed(full_path):
            abort(403, message="You are not allowed to this path")

        with open(full_path, 'w+') as fp:
            pass

        return {"message": "OK"}

    def delete(self):
        """
        Remove file from requested path
        """
        request_data = request.get_json(force=True)
        current_path = self.get_current_path()
        file_name = request_data.get('file_name')

        if not file_name:
            abort(400, message="File name must not be empty!")

        full_path = os.path.join(current_path, file_name)

        if not os.path.exists(full_path):
            abort(400, message="File was not found in current path!")

        if not os.path.isfile(full_path):
            abort(400, message="File name is not a file!")

        if not self.is_allowed(full_path):
            abort(403, message="You are not allowed to this path")

        os.remove(full_path)

        return {"message": "OK"}

    def put(self):
        """
        Set file that i want to get info
        """
        request_data = request.get_json(force=True)
        current_path = self.get_current_path()
        requested_file = request_data.get('file_name')

        if not requested_file:
            abort(400, message="File must not be empty")

        full_path = os.path.join(current_path, requested_file)

        if not os.path.exists(full_path):
            abort(404, message="Path was not found in the system!")

        if not os.path.isfile(full_path):
            abort(400, message="Path must lead to a file")

        if not self.is_allowed(full_path):
            abort(403, message="You are not allowed to this file")

        try:
            with open("requestedFile.txt", "w+") as f:
                path_correct_slashes = self.change_all_slashes(full_path)
                f.write(path_correct_slashes + "\n")
        except IOError:
            abort(500, message="Can not create file for allowed paths!")

        return {"message": "OK"}
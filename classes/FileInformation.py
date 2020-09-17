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
        request_data = request.get_json()
        requested_path = self.change_all_slashes(request_data['path'])
        if not requested_path:
            abort(400, message="Path must not be empty!")

        if not os.path.exists(requested_path):
            abort(404, message="Path was not found in the system!")

        if not os.path.isfile(requested_path):
            abort(400, message="Path must be a file")

        if self.is_allowed(requested_path):
            data = self.get_file_info(requested_path)
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
        request_data = request.get_json()
        requested_path = self.change_all_slashes(request_data['path'])
        file_name = request_data['file_name']
        full_path = os.path.join(requested_path, file_name)

        if not requested_path or not file_name:
            abort(400, message="Path and file name must not be empty!")

        if os.path.exists(full_path):
            abort(400, message="File already exists!")

        with open(full_path, 'w') as fp:
            pass

        return {"message": "OK"}

    def delete(self):
        """
        Remove file from requested path
        """
        request_data = request.get_json()
        requested_path = self.change_all_slashes(request_data['path'])

        if not requested_path:
            abort(400, message="Path must not be empty!")

        if not os.path.exists(requested_path):
            abort(400, message="Path was not found in the system!")

        if not os.path.isfile(requested_path):
            abort(400, message="Path does not contain a file!")

        os.remove(requested_path)

        return {"message": "OK"}
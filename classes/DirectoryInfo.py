from flask import request
from flask_restful import Resource, abort
from classes.RestrictionHelper import RestrictionHelper
import os


class DirectoryInfo(Resource, RestrictionHelper):
    def get(self):
        """
        Get information about requested path
        """
        data = []
        request_data = request.get_json()
        requested_path = self.change_all_slashes(request_data['path'])
        if not requested_path:
            abort(400, message="Path must not be empty")

        if not os.path.exists(requested_path):
            abort(404, message="Path was not found in the system!")

        if not os.path.isdir(requested_path):
            abort(400, message="Path must be a dicertory")

        if self.is_allowed(requested_path):
            data = self.get_directory_info(requested_path)
        else:
            abort(403, message="You are not allowed to this path")

        result = {"data": data, "count": len(data)}
        return result

    def get_directory_info(self, path):
        """
        Helping function for getting information about subfile and subdirectories
        """
        dirs = []
        for x in os.listdir(path):
            full_path = os.path.join(path, x)
            f = {
                "name": x,
                "created_at": os.path.getctime(full_path),
                "last_modification_at": os.path.getmtime(full_path),
                "size": os.path.getsize(full_path),
                "is_file": os.path.isfile(full_path),
                "is_dir": os.path.isdir(full_path),
            }
            dirs.append(f)

        return dirs

    def post(self):
        """
        Create directory with path and dir_name variables
        """
        request_data = request.get_json()
        requested_path = self.change_all_slashes(request_data['path'])
        dir_name = request_data['dir_name']
        full_path = os.path.join(requested_path, dir_name)

        if not requested_path or not dir_name:
            abort(400, message="Path and directory name must not be empty!")

        if os.path.exists(full_path):
            abort(400, message="Directory already exists!")

        os.makedirs(full_path)

        return {"message": "OK"}

    def delete(self):
        """
        Remove directory by requested path
        """
        request_data = request.get_json()
        requested_path = self.change_all_slashes(request_data['path'])

        if not requested_path:
            abort(400, message="Path must not be empty!")

        if not os.path.exists(requested_path):
            abort(400, message="Path was not found in the system!")

        if os.listdir(requested_path):
            abort(400, message="Directory is not empty")

        os.rmdir(requested_path)

        return {"message": "OK"}
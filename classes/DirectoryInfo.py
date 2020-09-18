from flask import request
from flask_restful import Resource, abort
from classes.RestrictionHelper import RestrictionHelper
import os


class DirectoryInfo(Resource, RestrictionHelper):
    def get(self):
        """
        Get information about current path
        """
        current_path = self.get_current_path()

        if not self.is_allowed(current_path):
            abort(403, message="You are not allowed to this path")

        data = []
        try:
            data = self.get_directory_info(current_path)
        except PermissionError:
            abort(403, message="Not Allowed there")

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
        request_data = request.get_json(force=True)
        current_path = self.get_current_path()
        dir_name = request_data.get('dir_name')

        if not dir_name:
            abort(400, message="Path and directory name must not be empty!")

        full_path = os.path.join(current_path, dir_name)

        if os.path.exists(full_path):
            abort(400, message="Directory already exists!")

        if not self.is_allowed(full_path):
            abort(403, message="You are not allowed to this path")

        os.makedirs(full_path)

        return {"message": "OK"}

    def delete(self):
        """
        Remove directory by requested path
        """
        request_data = request.get_json(force=True)
        current_path = self.get_current_path()
        requested_dir = request_data.get('dir_name')

        if not requested_dir:
            abort(400, message="Dir_name must not be empty!")

        full_path = os.path.join(current_path, requested_dir)

        if not os.path.exists(full_path):
            abort(400, message="Path was not found in the system!")

        if os.listdir(full_path):
            abort(400, message="Directory is not empty")

        if not self.is_allowed(full_path):
            abort(403, message="You are not allowed to this path")

        os.rmdir(full_path)

        return {"message": "OK"}

    def put(self):
        """
        Set current path into file
        """
        request_data = request.get_json(force=True)
        requested_path = self.change_all_slashes(request_data.get('path'))

        if not requested_path:
            abort(400, message="Path must not be empty")

        if not os.path.exists(requested_path):
            abort(404, message="Path was not found in the system!")

        if not os.path.isdir(requested_path):
            abort(400, message="Path must be a dicertory")

        if not self.is_allowed(requested_path):
            abort(403, message="You are not allowed to this path")

        try:
            with open("currentPath.txt", "w+") as f:
                path_correct_slashes = self.change_all_slashes(requested_path)
                f.write(path_correct_slashes + "\n")
        except IOError:
            abort(500, message="Can not create file for allowed paths!")

        return {"message": "OK"}
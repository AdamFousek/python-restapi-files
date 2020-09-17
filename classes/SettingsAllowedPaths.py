from flask import request
from flask_restful import Resource, abort
from classes.RestrictionHelper import RestrictionHelper
import os


class SettingsAllowedPaths(Resource):
    def get(self):
        """
        Get all paths from allowedPaths.txt file and return them
    
        """
        paths = []
        try:
            with open("allowedPaths.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    paths.append(line.strip())
        except IOError:
            abort(404, message="Allowed paths were not set yet!")

        return {"data": paths}

    def post(self):
        """
        Save paths into file, to check restrictions
        """
        request_data = request.get_json()
        paths = request_data['paths']
        try:
            with open("allowedPaths.txt", "w+") as f:
                for path in paths:
                    path_correct_slashes = self.change_all_slashes(path)
                    f.write(path_correct_slashes + "\n")
        except IOError:
            abort(500, message="Can not create file for allowed paths!")

        return {"message": "OK"}
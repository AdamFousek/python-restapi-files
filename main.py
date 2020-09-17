from flask import Flask, render_template, request
from flask_restful import Api, Resource, abort
import os

app = Flask(__name__,
            template_folder='.',
            static_folder=".",
            static_url_path="")

api = Api(app)


@app.route('/')
def index():
    return render_template('index.html')


def change_all_slashes(string):
    """
    Helping function for use right separator by OS
    """
    result = string.replace("/", os.path.sep)
    result = result.replace("\\", os.path.sep)
    return result


class RestrictionHelper():
    """
    Helper class for restriction
    """
    def is_allowed(self, path):
        """
        Function that return True / False depends on restriction
        """
        allowed_paths = self.get_allowed_paths()
        for allowed_path in allowed_paths:
            if allowed_path in path:
                return True

        return False

    def get_allowed_paths(self):
        """
        Return allowed paths for check if user allowed
        """
        paths = []
        try:
            with open("allowedPaths.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    paths.append(line.strip())
        except IOError:
            pass

        return paths


class SettingsAllowedPaths(Resource, RestrictionHelper):
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
                    path_correct_slashes = change_all_slashes(path)
                    f.write(path_correct_slashes + "\n")
        except IOError:
            abort(500, message="Can not create file for allowed paths!")

        return {"message": "OK"}


class DirectoryInfo(Resource, RestrictionHelper):
    def get(self):
        """
        Get information about requested path
        """
        data = []
        request_data = request.get_json()
        requested_path = change_all_slashes(request_data['path'])
        if not requested_path:
            abort(400, message="Path must not be empty")

        if not os.path.exists(requested_path):
            abort(404, message="Path was not found in the system!")

        if not os.path.isdir(requested_path):
            abort(400, message="Path must be dicertory")

        allowed_paths = self.get_allowed_paths()

        if not allowed_paths:
            abort(
                400,
                message=
                "Allowed paths were not set, you are not allowed to any path.")

        if self.is_allowed(requested_path):
            data = self.get_directory_info(requested_path)
        else:
            abort(403, message="You are not allowed to this path")

        result = {"data": data, "count": len(data)}
        return result

    def get_directory_info(self, path):
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


class FileInformation(Resource):
    def get(self):
        pass


api.add_resource(SettingsAllowedPaths, '/settings')
api.add_resource(DirectoryInfo, '/directory')

if __name__ == "__main__":
    app.run(host="localhost", port="7777", debug=True)
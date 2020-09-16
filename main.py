from flask import Flask, render_template, request
from flask_restful import Api, Resource, abort
from pathlib import Path

app = Flask(__name__,
            template_folder='.',
            static_folder=".",
            static_url_path="")

api = Api(app)


@app.route('/')
def index():
    return render_template('index.html')


class SettingsAllowedPaths(Resource):
    def get(self):
        """
        Get all paths from allowedPaths.txt file and return them
    
        """
        paths = []
        try:
            with open("allowedPaths.txt", "r") as f:
                lines = f.readlines()
                print(lines)
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
                    f.write(path + "\n")
        except IOError:
            abort(500, message="Can not create file for allowed paths!")

        return {"message": "OK"}


class DirectoryInfo():
    def get(self):
        """
        Get information about requested path
        """
        request_data = request.get_json()
        p = request_data['path']
        if not p:
            abort(400, message="Path must not be empty")

        path = Path(p)

        if not path.exists():
            abort(404, message="Path was not found in the system!")

        allowed_paths = self.getAllowedPaths()

        if not allowed_paths:
            abort(
                400,
                message=
                "Allowed paths were not set, you are not allowed to any path.")

        data = {}

        return {"data": data}

    def getAllowedPaths(self):
        """
        Return allowed paths for check if user allowed
        """
        paths = []
        try:
            with open("allowedPaths.txt", "r") as f:
                lines = f.readlines()
                print(lines)
                for line in lines:
                    paths.append(line.strip())
        except IOError:
            pass

        return paths


api.add_resource(SettingsAllowedPaths, '/settings')

if __name__ == "__main__":
    app.run(host="localhost", port="7777", debug=True)
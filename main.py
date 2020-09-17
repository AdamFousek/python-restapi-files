from flask import Flask, render_template, request
from flask_restful import Api, Resource, abort
import os
from classes import DirectoryInfo, FileInformation, SettingsAllowedPaths

app = Flask(__name__,
            template_folder='.',
            static_folder=".",
            static_url_path="")

api = Api(app)


@app.route('/')
def index():
    return render_template('index.html')


api.add_resource(SettingsAllowedPaths.SettingsAllowedPaths, '/settings')
api.add_resource(DirectoryInfo.DirectoryInfo, '/directory')
api.add_resource(FileInformation.FileInformation, '/file')

if __name__ == "__main__":
    app.run(host="localhost", port="7777", debug=True)
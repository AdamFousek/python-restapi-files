from flask import Flask, render_template
from flask_restful import Api, Resource

app = Flask(__name__)

app = Flask(__name__,
            template_folder='.',
            static_folder=".",
            static_url_path="")


@app.route('/')
def index():
    return render_template('index.html')


api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {"data": "Hello World"}


api.add_resource(HelloWorld, '/hello')

if __name__ == "__main__":
    app.run(host="localhost", port="7777", debug=True)
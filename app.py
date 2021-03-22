# flask packages
from flask import Flask, app
from flask_restx import Api

# local packages
from api.routes import create_routes

# default mongodb configuration
default_config = {
    'UPLOAD_FOLDER': 'uploads', 
    "SERVER_NAME": 'localhost:5000'}



def get_flask_app(config: dict = None) -> app.Flask:

    # init flask
    flask_app = Flask(__name__)

    # configure app
    config = default_config if config is None else config
    flask_app.config.update(config)


    # init api and routes
    api = Api(app=flask_app)
    create_routes(api=api)

    return flask_app


if __name__ == '__main__':
    # Main entry point when run in stand-alone mode.
    app = get_flask_app()
    app.run(debug=True)
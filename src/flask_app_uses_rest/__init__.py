from flask import Flask


def create_app():
    app = Flask(__name__)

    from flask_app_uses_rest.app_flask import main
    app.register_blueprint(main)

    return app

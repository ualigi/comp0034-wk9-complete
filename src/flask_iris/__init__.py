from flask import Flask
from flask_iris.create_ml_model import create_model


def create_app(config_object):
    """Create and configure the Flask app

    Args:
    config_object: configuration class (see config.py)

    Returns:
    Configured Flask app

    """
    app = Flask(__name__)

    app.config.from_object(config_object)

    # Include the routes from routes.py
    with app.app_context():
        from flask_iris import routes

    # If the ml model file isn't present, create it
    # Commented out, you will need to install scikit-learn if you want to run this
    # create_model("lr")

    return app

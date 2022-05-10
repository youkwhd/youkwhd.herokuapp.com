from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    register_blueprints(app)

    return app

def register_blueprints(app):
    from .views import blueprints

    for blueprint in blueprints.values():
        app.register_blueprint(blueprint)

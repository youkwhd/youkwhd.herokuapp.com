from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    register_blueprints(app)

    @app.errorhandler(404)
    def not_found(_):
        return render_template("404.html"), 404

    return app

def register_blueprints(app):
    from .views import blueprints

    for blueprint in blueprints.values():
        app.register_blueprint(blueprint)

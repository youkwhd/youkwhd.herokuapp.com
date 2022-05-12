from flask import Flask, render_template
from flask_flatpages import FlatPages

# all the posts from _posts directory
posts = FlatPages()

def create_app():
    app = Flask(__name__)

    # TODO: clean up these 3 lines
    app.config['FLATPAGES_EXTENSION'] = ".md"
    app.config['FLATPAGES_ROOT'] = "_posts"
    posts.init_app(app)

    register_blueprints(app)

    @app.errorhandler(404)
    def not_found(_):
        return render_template("404.html"), 404

    return app

def register_blueprints(app):
    from .views import blueprints

    for blueprint in blueprints.values():
        app.register_blueprint(blueprint)

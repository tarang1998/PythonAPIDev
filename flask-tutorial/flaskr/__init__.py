import os
from flask import Flask, render_template
from . import db
from . import auth
from . import blog


def create_app(test_config=None):

    # create and configure the app
    # __name__ is the name of the current Python module. 
    # The app needs to know where it’s located to set up some paths, and __name__ is a convenient way to tell it that.
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')



    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    return app
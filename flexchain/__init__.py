import os

from flask import Flask, render_template


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_folder="static/")
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_HOST=os.environ.get("DATABASE_HOST"),
        DATABASE_PORT=int(os.environ.get("DATABASE_PORT")),
        DATABASE_USER=os.environ.get("DATABASE_USER"),
        DATABASE_PASSWORD=os.environ.get("DATABASE_PASSWORD"),
        DATABASE=os.environ.get("DATABASE"),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    @app.route('/')
    def home_page():
        page_data = {
            'dashboard': True
        }
        return render_template("index.html", context=page_data)

    @app.route('/ask')
    def ask_page():
        return render_template("ask.html")

    @app.route('/404')
    def not_found_page():
        return render_template("404.html")

    @app.route('/account')
    def account_page():
        return render_template("account.html")

    from . import location
    app.register_blueprint(location.bp)

    from . import product
    app.register_blueprint(product.bp)

    from . import account
    app.register_blueprint(account.bp)

    from . import insights
    app.register_blueprint(insights.bp)

    from . import settings
    app.register_blueprint(settings.bp)

    return app

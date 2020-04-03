import os

from flask import session, Flask, render_template, request, redirect, url_for

from .auth import login_required, perform_login
from .models.chart_data import get_txn_amount, get_forecast_inventory
from .models.product import get_product_out, get_product_low


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

    from . import inventory
    inventory.init_app(app)

    @app.route('/')
    @login_required
    def home_page():
        page_data = {
            'dashboard': True,
            "count_stockout": 0,
            "count_critical": 0,
            "count_missingsales": 0,
            "data": [],
            "forecast": [],
            "name": "User"
        }
        connection = db.get_db()
        cursor = connection.cursor()
        page_data["count_stockout"] = len(get_product_out(cursor))
        page_data["count_critical"] = len(get_product_low(connection, cursor))
        # page_data["count_missingsales"] = len(get_missingdata(cursor))
        page_data['data'] = get_txn_amount(cursor)
        page_data['forecast'] = get_forecast_inventory(connection, cursor)
        page_data['name'] = session['auth'][request.remote_addr]
        print(page_data['forecast'])
        return render_template("index.html", context=page_data)

    @app.route('/answer')
    def answer_page():
        answer = request.args.get('answer', '')
        return render_template("answers.html", answer=answer)

    @app.route('/404')
    def not_found_page():
        return render_template("404.html")

    @app.route('/account')
    def account_page():
        return render_template("account.html")

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/login/attempt', methods=['POST'])
    def login_attempt():
        success = False
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        if email is None or password is None:
            print(email, password)
            print('Error here.')
        try:
            connection = db.get_db()
            cursor = connection.cursor()
            success = perform_login(cursor, email, password)
            cursor.close()
        except Exception as e:
            print(e)
        if success:
            return redirect(url_for('home_page'))
        return redirect(url_for('login'))

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

from flask import (
    Blueprint, render_template
)

from db import get_db
from models import location

bp = Blueprint('location', __name__, url_prefix='/location')


@bp.route('add-warehouse')
def add_warehouse():
    return render_template("location/add-warehouse.html")


@bp.route('adjust-inventory')
def adjust_inventory():
    return render_template("location/adjust-inventory.html")


@bp.route('find-store')
def find_store():
    page_data = {
        'stores': list()
    }
    connection = get_db()
    cursor = connection.cursor()
    try:
        page_data['stores'] = location.get_store(cursor)
    except Exception as e:
        print(e)
    return render_template("location/find-store.html", context=page_data)


@bp.route('find-warehouse')
def find_warehouse():
    return render_template("location/find-warehouse.html")


@bp.route('update-store')
def update_store():
    return render_template("location/update-store.html")


@bp.route('update-warehouse')
def update_warehouse():
    return render_template("location/update-warehouse.html")


@bp.route('warehouse')
def warehouse():
    return render_template("location/warehouse.html")


@bp.route('')
def location_index():
    return render_template("location/index.html")

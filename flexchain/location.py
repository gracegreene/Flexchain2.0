from flask import (
    Blueprint, render_template,
    request)

from db import get_db
from models import location, product, current_inventory

bp = Blueprint('location', __name__, url_prefix='/location')


@bp.route('add-store', methods=["GET", "POST"])
def add_store_page():
    connection = get_db()
    cursor = connection.cursor()
    if request.method == "POST":
        integration_id = request.form.get("")
        store_name = request.form.get()
        country = request.form.get()
        state = request.form.get()
        street_address = request.form.get()
        zip_code = request.form.get()
        coordinates = request.form.get()
        notes = request.form.get()
        loc = location.location(0, "store", store_name, country, state, street_address, zip_code, integration_id,
                                coordinates, notes, "Dress My Desk")
        sql = loc.insert(cursor)
        connection.commit()
        cursor.close()
        # redirect
    return render_template("location/add-store.html")


@bp.route('add-warehouse')
def add_warehouse():
    connection = get_db()
    cursor = connection.cursor()
    if request.method == "POST":
        integration_id = request.form.get("")
        store_name = request.form.get()
        country = request.form.get()
        state = request.form.get()
        street_address = request.form.get()
        zip_code = request.form.get()
        coordinates = request.form.get()
        notes = request.form.get()
        loc = location.location(0, "warehouse", store_name, country, state, street_address, zip_code, integration_id,
                                coordinates, notes, "Dress My Desk")
        sql = loc.insert(cursor)
        connection.commit()
        cursor.close()
        # redirect
    return render_template("location/add-warehouse.html")


@bp.route('adjust-inventory', methods=["GET", "POST"])
def adjust_inventory():
    page_data = {
        'locations': list(),
        'products': list(),
        'adjustment_reasons': [
            'Sale',
            'Pilferage',
            'Stock Transfer',
            'New Stocks Received',
            'Damage',
            'Other - Replenish',
            'Other - Transfer',
            'Other - Deplete'
        ]
    }
    connection = get_db()
    cursor = connection.cursor()
    if request.method == "POST":
        from_location = request.form.get('location-from')
        to_location = request.form.get('location-to')
        prod = request.form.get('product')
        reason = request.form.get('reason')
        quantity = request.form.get('quantity')
        try:
            # Reduction
            if reason == 0 or reason == 1 or reason == 4 or reason == 7:
                inventory = current_inventory.current_inventory(prod, 0, from_location)
                inventory.deplete(cursor, quantity, prod, from_location)
            # Addition
            if reason == 3 or reason == 5:
                inventory = current_inventory.current_inventory(prod, 0, from_location)
                inventory.replenish(cursor, quantity, prod, from_location)
            # Transfer
            if reason == 2 or reason == 6:
                inventory = current_inventory.current_inventory(prod, 0, from_location)
                inventory.transfer(cursor, quantity, prod, from_location, to_location)
        except Exception as e:
            print(e)
        cursor.close()
        connection.commit()
        return render_template("location/adjust-inventory.html", context=page_data)
    try:
        page_data['locations'] = location.get_all_locations(cursor)
        page_data['products'] = product.get_all_products(cursor)
    except Exception as e:
        print(e)
    cursor.close()
    return render_template("location/adjust-inventory.html", context=page_data)


@bp.route('add-vendor')
def add_vendor_page():
    connection = get_db()
    cursor = connection.cursor()
    if request.method == "POST":
        integration_id = request.form.get("")
        store_name = request.form.get()
        country = request.form.get()
        state = request.form.get()
        street_address = request.form.get()
        zip_code = request.form.get()
        coordinates = request.form.get()
        notes = request.form.get()
        loc = location.location(0, "vendor", store_name, country, state, street_address, zip_code, integration_id,
                                coordinates, notes, "Dress My Desk")
        sql = loc.insert(cursor)
        connection.commit()
        cursor.close()
        # redirect
    pass


@bp.route('find-vendor')
def find_vendor_page():
    pass


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
    page_data = {
        'warehouses': list()
    }
    connection = get_db()
    cursor = connection.cursor()
    try:
        page_data['warehouses'] = location.get_warehouse(cursor)
    except Exception as e:
        print(e)
    return render_template("location/find-warehouse.html", context=page_data)


@bp.route('update-store')
def update_store():
    return render_template("location/update-store.html")


@bp.route('update-warehouse')
def update_warehouse():
    return render_template("location/update-warehouse.html")


@bp.route('')
def location_index():
    return render_template("location/index.html")

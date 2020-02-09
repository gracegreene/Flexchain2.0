import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from .models import product
from .db import get_db

bp = Blueprint('product', __name__ , url_prefix='/product')


@bp.route('add')
def add_product():
    render_template('product/add-product.html')


@bp.route('archive')
def archive_product():
    render_template('product/archive-product.html')


@bp.route('')
def find_product():
    page_data = {
        "find_product_tab": True,
        "add_product_tab": False,
        "update_product_tab": False,
        "archive_product_tab": False,
        "log_sale_product_tab": False,
        "products": list(),
        "error": None,
    }
    query = request.args.get("name")
    if query is not None:
        # Perform the query here and update
        cursor = get_db().cursor()
        page_data["products"] = product.get_product(cursor, query)
        cursor.close()
    return render_template('product/find-product.html', context=page_data)


@bp.route('log-sales')
def log_sales():
    render_template('product/log-sales.html')


@bp.route('update')
def update():
    render_template('product/update-product.html')


@bp.route('update-form')
def update_form():
    render_template('product/update-form.html')

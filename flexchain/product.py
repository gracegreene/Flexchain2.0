from flask import (
    Blueprint, flash, redirect, render_template, request
)

from .models import product, transaction, mysql_generic, location
from .db import get_db

bp = Blueprint('product', __name__, url_prefix='/product')


@bp.route('add', methods=["GET", "POST"])
def add_product_page():
    page_data = {
        'errors': None,
    }
    if request.method == "POST":
        sku = request.form.get("SKU")
        product_name = request.form.get("Product-Name")
        description = request.form.get("Description")
        unit_cost = request.form.get("Unit-Cost-2")
        weight = request.form.get("Weight")
        length = request.form.get("Length")
        width = request.form.get("Width")
        height = request.form.get("Height")
        case_size = request.form.get("Case-Size")
        wholesale_price = request.form.get("Wholesale-Price")
        retail_price = request.form.get("Retail-Price")
        image_path = request.form.get("Image-Path")
        collection = request.form.get("Collection")
        # TODO Validate form
        # Attempt to insert into database
        p = product.product(sku, product_name, description, retail_price, unit_cost, weight, company_code="DMD",
                            length=length, width=width, height=height, case_size=case_size,
                            wholesale_price=wholesale_price,
                            image_path=image_path, collection=collection)
        sql, data = p.insert_statement_and_data()
        connection = get_db()
        cursor = connection.cursor()
        try:
            cursor.execute(sql, data)
            get_db().commit()
        except Exception as e:
            flash("There was an error saving the product to the database: ", e)
            page_data["errors"] = e
        cursor.close()
    return render_template('product/add-product.html')


@bp.route('archive', methods=["GET", "POST"])
def archive_product_page():
    page_data = {
        'products': list()
    }
    sku = request.args.get('sku')
    cursor = get_db().cursor()
    if sku is not None:
        try:
            page_data['products'] = product.get_product(cursor, sku)
        except Exception as e:
            print(e)
    cursor.close()
    return render_template('product/archive-product.html', context=page_data)


@bp.route('<sku>/archive')
def archive_product(sku):
    connection = get_db()
    cursor = connection.cursor()
    try:
        p = product.get_single_product(cursor, sku)
        p.archive = True
        p.update(cursor)
        connection.commit()
    except Exception as e:
        print(e)
    cursor.close()
    return redirect("/product/archive")


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


@bp.route('log', methods=["GET", "POST"])
def log_sales():
    page_data = {
        'locations': list(),
        'products': list(),
    }
    connection = get_db()
    if request.method == "POST":
        date = request.form.get("Date")
        total_sale = request.form.get("Total-Amount")
        selected_location = request.form.get("Location")
        product_sales = [
            {'sku': request.form.get("SKU-0"), 'quantity': request.form.get("Quantity-0")},
            {'sku': request.form.get("SKU-1"), 'quantity': request.form.get("Quantity-1")},
            {'sku': request.form.get("SKU-2"), 'quantity': request.form.get("Quantity-2")},
            {'sku': request.form.get("SKU-3"), 'quantity': request.form.get("Quantity-3")}
        ]
        cursor = connection.cursor()
        try:
            new_transaction = transaction.Transaction(date, total_sale, selected_location)
            new_transaction.create(cursor, "deplete", "sale")
            new_transaction_id = mysql_generic.get_last_insert_id(cursor)[0]
            for sale in product_sales:
                if sale['sku'] is not None and sale['quantity'] is not None:
                    transaction_sku = transaction.TransactionSKU(sale['sku'], sale['quantity'])
                    transaction_sku.create(cursor, new_transaction_id)
            connection.commit()
        except Exception as e:
            print(e)
        cursor.close()
    cursor = connection.cursor()
    try:
        page_data['products'] = product.get_all_products(cursor)
        page_data['locations'] = location.get_all_locations(cursor)
    except Exception as e:
        print(e)
    cursor.close()
    return render_template('product/log-sales.html', context=page_data)


@bp.route('update', methods=["GET", "POST"])
def update():
    page_data = {
        'products': list()
    }
    connection = get_db()
    query = request.args.get("name-4")
    if query is not None:
        # Perform the query here and update
        cursor = connection.cursor()
        page_data["products"] = product.get_product(cursor, query)
        cursor.close()
    return render_template('product/update-product.html', context=page_data)


@bp.route('update-form', methods=["GET", "POST"])
def update_form():
    page_data = {
        "errors": None,
    }
    connection = get_db()
    if request.method == "POST":
        # Get form values here
        # Validate values
        cursor = connection.cursor()
        try:
            sku = request.form.get("SKU")
            selected_product = product.get_single_product(cursor, sku)
            print(selected_product)
            selected_product.prod_name = request.form.get("Product-Name")
            selected_product.description = request.form.get("Description")
            selected_product.unit_cost = float(request.form.get("Unit-Cost-2"))
            if request.form.get("Weight"):
                selected_product.weight = float(request.form.get("Weight"))
            else:
                selected_product.weight = 0
            if request.form.get("Length"):
                selected_product.length = float(request.form.get("Length"))
            else:
                selected_product.length = 0
            if request.form.get("Width"):
                selected_product.width = float(request.form.get("Width"))
            else:
                selected_product.width = 0
            if request.form.get("Height"):
                selected_product.height = float(request.form.get("Height"))
            else:
                selected_product.height = 0
            selected_product.case_size = int(request.form.get("Case-Size"))
            selected_product.wholesale_price = float(request.form.get("Wholesale-Price"))
            selected_product.retail_price = float(request.form.get("Retail-Price"))
            selected_product.image_path = request.form.get("Image-Path")
            if request.form.get("Collection"):
                selected_product.collection = request.form.get("Collection")
            else:
                selected_product.collection = ""
            selected_product.update(cursor)
            cursor.close()
            connection.commit()
        except Exception as e:
            print(e)
            cursor.close()
            page_data["errors"] = list(e)
            return render_template("/product/update-product.html", context=page_data)
        return render_template("/product/update-product.html", context=page_data)
    sku = request.args.get("sku")
    if sku is None:
        return render_template("/product/update-product.html", context=page_data)
    cursor = connection.cursor()
    selected_product = product.get_single_product(cursor, sku)
    cursor.close()
    page_data["sku"] = sku
    page_data['product'] = selected_product
    return render_template("/product/update-form.html", context=page_data)

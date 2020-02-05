from flask import Flask
from flask import render_template #to render html
from flask import request #to check details about the incoming request
from flask import redirect
from flexchain.models import location, product, mysql_generic, transaction
import mysql.connector
import json
app = Flask(__name__, template_folder="WebFrontEndCode/templates", static_folder="WebFrontEndCode/static/")

connection = mysql.connector.connect(
    host="flexchain-db.c9c4zw0dc4zn.us-east-2.rds.amazonaws.com",
    port=3306,
    user="admin",
    password='w0BtB6lVyAnqG2zMg4R5',
    database='innodb'
)


@app.route('/')
@app.route('/index.html')
def home_page():
    return render_template("flexchain/templates/index.html")


@app.route('/ask.html')
def ask_page():
    return render_template("flexchain/templates/ask.html")


@app.route('/dashboard-settings.html')
def dashboard_settings_page():
    return render_template("flexchain/templates/dashboard-settings.html")


@app.route('/location/adjust/inventory', methods=["POST"])
def adjust_inventory():
    page_data = {
        "company_locations_data": list(),
    }
    cursor = connection.cursor()
    try:
        all_data = location.get_store(cursor)
        warehouse_data = location.get_warehouse(cursor)
    except Exception as e:
        print(e)
        # TODO 500 / error here
        cursor.close()
        return
    for data in warehouse_data:
        all_data.append(data)
    page_data["company_locations_data"] = all_data
    cursor.close()
    return render_template("flexchain/templates/locations.html", context=page_data)


@app.route('/locations.html', methods=["GET", "POST"])
def location_page():
    page_data = {}
    # page_data = {
    #     "store_tab": True,
    #     "warehouse_tab": False,
    #     "customer_tab": False,
    #     "update inventory_tab": False,
    #     "archive_location_tab": False,
    #     "error": None,
    #     "store_data": list(),
    #     "warehouse_data": list(),
    #     "customer_data": list(),
    # }
    #
    # cursor = connection.cursor()
    # page_data["customer_data"] = location.get_customer(cursor)
    # page_data["store_data"] = location.get_store(cursor)
    # page_data["warehouse_data"] = location.get_warehouse(cursor)
    #
    # if request.method == "POST":
    #     page_data["find_product_tab"] = False
    #     page_data["add_product_tab"] = True
    #     sku = request.form.get("SKU")
    #     product_name = request.form.get("Product-Name")
    #     description = request.form.get("Description")
    #     unit_cost = request.form.get("Unit-Cost")
    #     weight = request.form.get("Weight")
    #     length = request.form.get("Length")
    #     width = request.form.get("Width")
    #     height = request.form.get("Height")
    #     case_size = request.form.get("Case-Size")
    #     whole_sale_price = request.form.get("Wholesale-Price")
    #     retail_price = request.form.get("Retail-Price")
    #     # TODO Missing Company Code
    #
    #     p = product.product(sku,product_name,description,retail_price, unit_cost, weight, company_code="DMD",
    #                         length=None, width=None, height=None,case_size=case_size, wholesale_price=whole_sale_price,
    #                         image_path=None, collection=None)
    #     sql, data = p.insert_statement_and_data()
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute(sql, data)
    #         connection.commit()
    #     except Exception as e:
    #         print("There was an error saving the product to the database: ", e)
    #         page_data["error"] = e
    #     cursor.close()
    # else:
    #     query = request.args.get("q")
    #     if query is not None:
    #         # Perform the query here and update
    #         cursor = connection.cursor()
    #         page_data["products"] = product.get_product(cursor, query)
    #         cursor.close()
    #
    # print(page_data)
    return render_template("flexchain/templates/locations.html", context=page_data)


@app.route("/product/update-form.html", methods=["GET", "POST"])
def update_form_page():
    page_data = {
        "errors": None,
    }

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


@app.route("/product/update-product.html")
def update_product_page():
    page_data = {
        "errors": None,
    }
    query = request.args.get("name-4")
    if query is not None:
        # Perform the query here and update
        cursor = connection.cursor()
        page_data["products"] = product.get_product(cursor, query)
        cursor.close()
    return render_template("flexchain/templates/product/update-product.html", context=page_data)


@app.route('/product/add-product.html', methods=["GET", "POST"])
def add_product_page():
    page_data = {
        "errors": None,
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
                            length=length, width=width, height=height, case_size=case_size, wholesale_price=wholesale_price,
                            image_path=image_path, collection=collection)
        sql, data = p.insert_statement_and_data()
        cursor = connection.cursor()
        try:
            cursor.execute(sql, data)
            connection.commit()
        except Exception as e:
            print("There was an error saving the product to the database: ", e)
            page_data["errors"] = e
        cursor.close()
        # Redirect to new add page, should have some sort of confirmation of success
    return render_template("flexchain/templates/product/add-product.html", context=page_data)


@app.route('/product/archive-product', methods=["GET", "POST"])
@app.route('/product/archive-product.html', methods=["GET", "POST"])
def archive_product_page():
    page_data = {
        'products': list(),
    }
    sku = request.args.get('sku')
    cursor = connection.cursor()
    if sku is not None:
        try:
            page_data['products'] = product.get_product(cursor, sku)
        except Exception as e:
            print("here")
            print(e)
    cursor.close()
    return render_template("flexchain/templates/product/archive-product.html", context=page_data)


@app.route('/product/<sku>/archive')
def archive_product(sku):
    cursor = connection.cursor()
    try:
        p = product.get_single_product(cursor, sku)
        p.archive = True
        p.update(cursor)
        connection.commit()
    except Exception as e:
        print(e)
    cursor.close()
    return redirect("/product/archive-product.html")


@app.route('/product/log-sales.html', methods=["GET", "POST"])
def log_sales_page():
    page_data = {
        'locations': list(),
        'products': list(),
    }
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
            new_transaction_id = mysql_generic.get_last_insert_id(cursor)
            connection.commit()
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
    return render_template("flexchain/templates/product/log-sales.html", context=page_data)


@app.route('/product/find-product.html')
@app.route('/product')
def search_product_page():
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
        cursor = connection.cursor()
        page_data["products"] = product.get_product(cursor, query)
        cursor.close()
    return render_template("/product/find-product.html", context=page_data)


@app.route('/settings.html')
def settings_page():
    return render_template("flexchain/templates/settings.html")


@app.route('/api/v1/inventory/stockout')
def stockout_inventory_api():
    stockout_response = {
        "count": 0,
        "stockout_collection": list(),
    }
    # query
    find_stockout_sql = '''
    select product.sku, sum(quantity) from product
    left join current_inventory on product.sku = current_inventory.sku
    group by prod_name
    '''
    # set the count
    cursor = connection.cursor()
    try:
        cursor.execute(find_stockout_sql)
    except Exception as e:
        # 500 error
        print(e)
        cursor.close()
        return json.dumps({})
    for (sku, sum) in cursor:
        print(sku, sum)
        if sum is not None and sum == 0:
            stockout_response["stockout_collection"].append(sku)
    stockout_response["count"] = len(stockout_response["stockout_collection"])
    # set the collection
    # handle errors
    cursor.close()
    return json.dumps(stockout_response)


@app.route("/location/find-store.html")
def find_store_page():
    render_template("flexchain/templates/location/find-store.html")


@app.route("/location/update-store.html")
def update_store_details_page():
    render_template("flexchain/templates/location/update-store.html")


@app.route("/location/archive-location.html")
def archive_store():
    pass


@app.route("/location/find-warehouse.html")
def warehouse_page():
    render_template("flexchain/templates/location/find-warehouse.html")


@app.route("/location/update-warehouse.html")
def update_warehouse_page():
    render_template("flexchain/templates/location/update-warehouse.html")


@app.route("/location/archive-warehouse")
def archive_warehouse():
    pass


@app.route("/location/adjust-inventory.html")
def adjust_inventory_page():
    render_template("flexchain/templates/location/adjust-inventory.html")



if __name__ == '__main__':
    app.run()

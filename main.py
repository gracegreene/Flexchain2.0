from flask import Flask
from flask import render_template #to render html
from flask import request #to check details about the incoming request
from FlexchainDB import product
import mysql.connector
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
    return render_template("index.html")


@app.route('/ask.html')
def ask_page():
    return render_template("ask.html")


@app.route('/dashboard-settings.html')
def dashboard_settings_page():
    return render_template("dashboard-settings.html")


@app.route('/locations.html')
def location_page():
    return render_template("locations.html")


@app.route('/product.html', methods=["GET", "POST"])
def product_page():
    page_data = {
        "find_product_tab": True,
        "add_product_tab": False,
        "update_product_tab": False,
        "archive_product_tab": False,
        "log_sale_product_tab": False,
        "products": list(),
        "error": None,
    }

    if request.method == "POST":
        page_data["find_product_tab"] = False
        page_data["add_product_tab"] = True
        sku = request.form.get("SKU")
        product_name = request.form.get("Product-Name")
        description = request.form.get("Description")
        unit_cost = request.form.get("Unit-Cost")
        weight = request.form.get("Weight")
        length = request.form.get("Length")
        width = request.form.get("Width")
        height = request.form.get("Height")
        case_size = request.form.get("Case-Size")
        whole_sale_price = request.form.get("Wholesale-Price")
        retail_price = request.form.get("Retail-Price")
        # TODO Missing Company Code

        p = product.product(sku,product_name,description,retail_price, unit_cost, weight, company_code="DMD",
                            length=None, width=None, height=None,case_size=case_size, wholesale_price=whole_sale_price,
                            image_path=None, collection=None)
        sql, data = p.insert_statement_and_data()
        cursor = connection.cursor()
        try:
            cursor.execute(sql, data)
            connection.commit()
        except Exception as e:
            print("There was an error saving the product to the database: ", e)
            page_data["error"] = e
        cursor.close()
    else:
        query = request.args.get("q")
        if query is not None:
            # Perform the query here and update
            cursor = connection.cursor()
            page_data["products"] = product.get_product(cursor, query)
            cursor.close()
    return render_template("product.html", context=page_data)


@app.route('/settings.html')
def settings_page():
    return render_template("settings.html")


if __name__ == '__main__':
    app.run()

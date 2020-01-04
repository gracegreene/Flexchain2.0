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


@app.route('/product.html', methods=["GET","POST"])
def product_page():
    page_data = {
        "find_product_tab": True,
        "add_product_tab": False,
        "update_product_tab": False,
        "archive_product_tab": False,
        "log_sale_product_tab": False,
    }

    if request.method == "POST":
        page_data["find_product_tab"] = False
        page_data["add_product_tab"] = True
        sku = request.form.get("SKU")
        product_name = request.form.get("Product-Name")
        description = request.form.get("Description")
        unit_cost = request.form.get("Unit-Cost")
        weight = request.form.get("Weight")
        dimension = request.form.get("Dimension")
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
        except Exception as e:
            cursor.close()
            print("There was an error saving the product to the database: ", e)
            return render_template("product.html", context=page_data) # TODO error message
        connection.commit()
        cursor.close()
        return render_template("product.html") # TODO success message
    return render_template("product.html", context=page_data)


@app.route('/settings.html')
def settings_page():
    return render_template("settings.html")


if __name__ == '__main__':
    app.run()

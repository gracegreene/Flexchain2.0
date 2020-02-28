import math
from .db import get_db
from .forecast import forecast
from .models.product import get_product_out, get_product_low
from flask import (
    Blueprint, render_template, request
)

bp = Blueprint('insight', __name__, url_prefix="/insight")


@bp.route('/')
def get_insight_page():
    return render_template("ask.html")


@bp.route('stock-level')
def get_stock_level_page():
    page_data = {
        "products": list()
    }
    connection = get_db()
    cursor = connection.cursor()
    product_collection = list()

    if request.args.get("type") == "out":
        product_collection = get_product_out(cursor)
    elif request.args.get("type") == "low":
        product_collection = get_product_low(cursor)
    else:
        out_products = get_product_out(cursor)
        low_products = get_product_low(cursor)
        for p in out_products:
            product_collection.append(p)
        for p in low_products:
            # Need to filter out from getting double products here.
            add = True
            for pc in product_collection:
                if pc["sku"] == p["sku"]:
                    add = False
            if add:
                product_collection.append(p)

    for prod in product_collection:
        fc = forecast(4, 1, 0, prod["sku"], 1, connection)
        if len(fc) != 0:
            prod["demand"] = math.ceil(fc[0])
        else:
            prod["demand"] = "Forecast values cannot be generated at this time"

    page_data["products"] = product_collection
    # Create a function in the product model that returns the list of out of inventory / low items
    # Call the function here
    # Loop over the items
    # Add the forecast for each
    # After that add it to page_data and we can loop over it in the html. (I'll help with this part)
    # forecast(4,1,0,sku,1,connection)

    return render_template("stock-levels.html", context=page_data)

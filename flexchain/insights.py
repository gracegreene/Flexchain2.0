import math
from datetime import datetime, timedelta

from flask import (
    Blueprint, render_template, request, redirect, url_for
)

from .db import get_db
from .forecast import forecast
from .models.location import get_all_locations
from .models.product import get_product_out, get_product_low, get_all_products, get_itr, get_ROP

bp = Blueprint('insight', __name__, url_prefix="/insight")


@bp.route('/')
def get_insight_page():
    page_data = {
        'products': list(),
        'locations': list(),
        "count_stockout": 0,
        "count_critical": 0,
        "count_missingsales": 0
    }
    connection = get_db()
    cursor = connection.cursor()
    try:
        page_data["count_stockout"] = len(get_product_out(cursor))
        page_data["count_critical"] = len(get_product_low(cursor))
        # page_data["count_missingsales"] = len(get_missingdata(cursor))
        page_data['products'] = get_all_products(cursor)
        page_data['locations'] = get_all_locations(cursor)
    except Exception as e:
        print(e)
    return render_template("ask.html", context=page_data)


@bp.route('/ask/sell/what',  methods=["POST"])
def what_should_sell():
    answer = 'Flexchain recommends selling the following products as they have a high inventory turnover ratio in the location you indicated. You still have enough time to order more stocks for those in low supply.'
    form_location = request.form.get('location', None)
    form_date = request.form.get('date', None)
    sale_date = None
    if form_date:
        sale_date = datetime.strptime(form_date, '%Y-%m-%d')
    current_date = datetime.now()

    try:
        connection = get_db()
        cursor = connection.cursor()
        # Sale event less than 3 months: Get products and rank them according to ITR
        # filter out products in critical level and return up to 3
        if current_date + timedelta(days=90) > sale_date:
            product_itr = get_itr(cursor)
            product_filter = get_product_low(cursor)
            filtered_location_itr = [itr for itr in product_itr if int(itr['location']) == int(form_location)]
            print(filtered_location_itr)
            filtered_itr = [itr for itr in filtered_location_itr if itr['sku'] not in product_filter]
            # TODO redirect to html page where this can be structured.
            if len(filtered_itr) > 0:
                answer += "<ol>"

            for product in filtered_itr[0:3]:
                answer += '<li>' + product['name'] + '</li>'

            if len(filtered_itr) > 0:
                answer += "</ol>"

        # If date is more than 3 months:
        # get products and rank them according to ITR return top 3, filter out products in critical
        # and inform the user to order them ASAP
        else:
            product_itr = get_itr(cursor)
            product_filter = get_product_low(cursor)
            filtered_location_itr = [itr for itr in product_itr if int(itr['location']) == int(form_location)]
            for itr in filtered_location_itr:
                if itr['sku'] in product_filter:
                    itr['level'] = 'critical'
                else:
                    itr['level'] = 'stable'

            # TODO redirect to html page where this can be structured.
            if len(filtered_location_itr) > 0:
                answer += "<ol>"

            for product in filtered_location_itr[0:3]:
                answer += '<li>' + product['name'] + '</li>'

            if len(filtered_location_itr) > 0:
                answer += "</ol>"

    except Exception as e:
        print(e)
    return redirect(url_for('answer_page', answer=answer))


@bp.route('/ask/sell/where', methods=["POST"])
def where_should_sell():
    answer = "Flexchain recommends selling from or shipping from <insert location>. Data shows that the specific product you indicated sells really well in <insert location>."
    form_location = request.form.get('location', None)
    items = list()
    if form_location is None:
        # Need to redirect back with error here.
        print('Form location was blank 500.')
        return
    # Calculate ITR of 3 items in each location return location with highest ITR
    try:
        connection = get_db()
        cursor = connection.cursor()
        products = get_all_products(cursor)
        for p in products:
            include = request.form.get(p["sku"], None)
            if include is not None:
                items.append(p["sku"])
        product_itr = get_itr(cursor)
        filtered_itr = [itr for itr in product_itr if itr['location'] == form_location]
        filtered_item_itr = [itr for itr in filtered_itr if itr['sku'] in items]
        print(filtered_item_itr
        cursor.close()
        # Answer: Flexchain recommends selling from or shipping from <insert location>. Data shows that the specific product you indicated sells really well in <insert location>.
    except Exception as e:
        print(e)
    return render_template("answers.html", answer=answer)


@bp.route('/ask/sell/should',  methods=["POST"])
def should_sell_item():
    form_product = request.form.get('product', None)
    form_location = request.form.get('location', None)
    # Get ITR of specific to store
    try:
        connection = get_db()
        cursor = connection.cursor()
        product_itr = get_itr(cursor)
        
        cursor.close()
    except Exception as e:
        print(e)
    # GET ITR of the rest of the items
    # Return rank of ITR of item with respect to the rest of the store and current inventory level
    # Answer: <Insert name of product> has <ITR> turns per year. It is taking 12/<ITR> months to sell and replace inventory.
    # Answer: If item is in top 3 ITR: You should definitely sell <Insert product name> as it is one of your top selling item in <location>
    # Answer: If item is bottom in ITR rank: It is best to find another item as <insert product name> is not selling well in <location>
    pass


@bp.route('/ask/order/quantity',  methods=["POST"])
def suggest_order_quantity():
    # Return order quantity and ROP (to tell the user that when current inventory in store x is below top,
    # you should order x amount
    form_product = request.form.get('product', None)
    form_location = request.form.get('location', None)
    try:
        connection = get_db()
        cursor = connection.cursor()
        rop = get_ROP(form_product)
        cursor.close()
    except Exception as e:
        print(e)

    pass


@bp.route('/ask/order/when',  methods=["POST"])
def when_order():
    # Get current inventory of store
    # if less than critical level:
    #    get next 3 month demand forecast
    #    return month 0 meaning to order now because of the demand forecasted is x for the next 3 months
    #Answer: Order <product name> now as current available inventory is in critical level. In the next 3 months, Flexchain predicts that you will have a demand of x units.

    # If more than critical level:
    # get reorder point
    # get next month forecast
    # get current inventory-next month forecast
    # if < reorder point
    # return month 1 and demand for next month that needs to be fulfilled, repeat loop until less than reorder point
    #Answer: 
    pass


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

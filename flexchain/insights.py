import math
from datetime import datetime, timedelta

from flask import (
    Blueprint, render_template, request, redirect, url_for, session
)

from .auth import login_required
from .db import get_db
from .forecast import forecast
from .models.current_inventory import get_current_inventory
from .models.location import get_all_locations, get_location_name_by_id
from .models.product import get_product_out, get_product_low, get_all_products, get_itr, get_ROP, get_product, \
    get_order_quantity

bp = Blueprint('insight', __name__, url_prefix="/insight")


@bp.route('/')
@login_required
def get_insight_page():
    page_data = {
        'products': list(),
        'locations': list(),
        "count_stockout": 0,
        "count_critical": 0,
        "count_missingsales": 0,
        "name": session['auth'][request.remote_addr]
    }
    connection = get_db()
    cursor = connection.cursor()
    try:
        page_data["count_stockout"] = len(get_product_out(cursor))
        page_data["count_critical"] = len(get_product_low(connection, cursor))
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
            product_filter = get_product_low(connection, cursor)
            filtered_location_itr = [itr for itr in product_itr if int(itr['location']) == int(form_location)]
            print(filtered_location_itr)
            filtered_itr = [itr for itr in filtered_location_itr if itr['sku'] not in product_filter]
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
            product_filter = get_product_low(connection, cursor)
            filtered_location_itr = [itr for itr in product_itr if int(itr['location']) == int(form_location)]
            for itr in filtered_location_itr:
                if itr['sku'] in product_filter:
                    itr['level'] = 'critical'
                else:
                    itr['level'] = 'stable'

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
    answer = ''
    answer_template = "Flexchain recommends selling from or shipping from {}. Data shows that the {} you indicated sells really well in {}."
    form_location = request.form.get('location', None)
    items = list()
    if form_location is None:
        # Need to redirect back with error here.
        print('Form location was blank 500.')
        return
    # Calculate ITR of items in each location return location with highest ITR
    try:
        connection = get_db()
        cursor = connection.cursor()
        products = get_all_products(cursor)
        for p in products:
            include = request.form.get(p["sku"], None)
            if include is not None:
                items.append(p["sku"])
        product_itr = get_itr(cursor)
        filtered_itr = [itr for itr in product_itr if int(itr['location']) == int(form_location)]
        filtered_item_itr = [itr for itr in filtered_itr if itr['sku'] in items]
        skus = [itr['sku'] for itr in filtered_item_itr]
        for i in filtered_item_itr[0:len(items)]:
            location_name = get_location_name_by_id(cursor, i['location'])
            answer += answer_template.format(location_name, i['name'], location_name) + '<br><br>'
        for item in items:
            if item not in skus:
                product = get_product(cursor, item)[0]
                answer += "There is not enough inventory or sales data to provide a recommendation for {}.<br><br>".format(
                    product['product_name']
                )
        cursor.close()
    except Exception as e:
        print(e)
    return render_template("answers.html", answer=answer)


@bp.route('/ask/sell/should', methods=["POST"])
def should_sell_item():
    chosen_itr = None
    answer = '''
    {} has {:0.0f} cycles per year. It is taking {:0.2f} months to sell and replace inventory.
    '''
    form_product = request.form.get('product', None)
    form_location = request.form.get('location', None)
    # Get ITR of specific to store
    try:
        connection = get_db()
        cursor = connection.cursor()
        product_itr = get_itr(cursor)
        filtered_itr = [itr for itr in product_itr if int(itr['location']) == int(form_location)]
        for itr in filtered_itr:
            if str(itr['sku']) == str(form_product):
                chosen_itr = itr
        if chosen_itr is None:
            answer = 'There is not enough sales and/or inventory data to provide a smart recommendation.'
            return render_template('answers.html', answer=answer)
        skus = [itr['sku'] for itr in filtered_itr[0:3]]
        product_name = get_product(cursor, form_product)[0]['product_name']
        location_name = get_location_name_by_id(cursor, form_location)
        answer = answer.format(product_name, chosen_itr['itr'], 12.0 / float(chosen_itr['itr']))
        if form_product in skus:
            answer += '<br>' + 'You should definitely sell {} as it is one of your top selling items in {}.'.format(
                product_name, location_name
            )
        else:
            answer += '<br>' + 'It is best to find another item as {} is not selling well in {}.'.format(
                product_name, location_name
            )
        cursor.close()
    except Exception as e:
        print(e)
    # GET ITR of the rest of the items
    # Return rank of ITR of item with respect to the rest of the store and current inventory level
    # Answer: <Insert name of product> has <ITR> turns per year. It is taking 12/<ITR> months to sell and replace inventory.
    # Answer: If item is in top 3 ITR: You should definitely sell <Insert product name> as it is one of your top selling item in <location>
    # Answer: If item is bottom in ITR rank: It is best to find another item as <insert product name> is not selling well in <location>
    return render_template('answers.html', answer=answer)


@bp.route('/ask/order/quantity',  methods=["POST"])
def suggest_order_quantity():
    # Return order quantity and ROP (to tell the user that when current inventory in store x is below top,
    # you should order x amount
    # Answer: Flexchain recommends ordering x amount of <product name> once available inventory is below <ROP>
    # order quantity function for x
    answer = 'Flexchain recommends ordering {:.0f} {} once available inventory is below {:.0f}.'
    form_product = request.form.get('product', None)
    try:
        connection = get_db()
        cursor = connection.cursor()
        rop = get_ROP(connection, form_product)
        product = get_product(cursor, form_product)[0]
        order_quantity = get_order_quantity(connection, cursor, form_product)
        answer = answer.format(order_quantity, product['product_name'], rop, order_quantity)
        cursor.close()
    except Exception as e:
        print(e)
    return render_template('answers.html', answer=answer)


@bp.route('/ask/order/when',  methods=["POST"])
def when_order():
    # Get current inventory
    # if less than critical level:
    #    get next 3 month demand forecast
    #    return month 0 meaning to order now because of the demand forecasted is x for the next 3 months
    # Answer: Order <product name> now as current available inventory is in critical level. In the next 3 months, Flexchain predicts that you will have a demand of x units.

    # If more than critical level:
    # get reorder point
    # get next month forecast
    # get current inventory-next month forecast
    # if < reorder point
    # return month 1 and demand for next month that needs to be fulfilled, repeat loop until less than reorder point
    # Answer: Order <insert product name> next month. While you still have x in your current inventory, it will not be enough to cover the demand anticipated for next month which is at x units.
    form_product = request.form.get('product', None)
    try:
        connection = get_db()
        cursor = connection.cursor()
        low_products = get_product_low(connection, cursor)
        low_products_sku = [p['sku'] for p in low_products]
        prod = get_product(cursor, form_product)[0]
        current_inventory = get_current_inventory(cursor, form_product)
        if form_product in low_products_sku:
            fc = forecast(4, 1, 0, form_product, 3, connection)
            answer = 'Order {} now as current available inventory is in critical level. In the next 3 months, ' \
                     'Flexchain predicts you will have a demand of {} units'
            return render_template('answers.html', answer=answer.format(prod['product_name'], sum(fc)))
        else:
            reorder_point = get_ROP(connection, form_product)
            fc = 0
            months = 0
            while float(reorder_point) < float(current_inventory) - float(fc):
                if months == 12:
                    return render_template('answers.html', answer="You will not have to order {} for at least another "
                                                                  "year.".format(prod['product_name']))
                months += 1
                fc = sum(forecast(4, 1, 0, form_product, months, connection))
                if fc == 0:
                    print(forecast(4, 1, 0, form_product, months, connection))
                    return render_template('answers.html', answer='Not enough data exists to determine when to '
                                                                  'reorder {} again.'.format(prod['product_name']))
                print(reorder_point, fc, months)
            answer = 'Order {} in {} month(s). You have {} in your current inventory to ' \
                     'to cover the demand anticipated for the next {} month(s) which is {:.0f} units. '
            return render_template('answers.html',
                                   answer=answer.format(prod['product_name'], months-1, current_inventory, months, fc))
    except Exception as e:
        print(e)
    return render_template('answers.html', answer=answer)


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
        product_collection = get_product_low(connection, cursor)
    else:
        out_products = get_product_out(cursor)
        low_products = get_product_low(connection, cursor)
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
            rop = get_ROP(connection, prod['sku'])
            order_quantity = get_order_quantity(connection, cursor, prod['sku'])
            prod["action"] = "Order {} units of {} once current inventory hits below {} units.".format(int(order_quantity), prod['product_name'], int(rop))
        else:
            prod["demand"] = "Forecast values cannot be generated at this time"
            prod["action"] = ""

    page_data["products"] = product_collection
    # Create a function in the product model that returns the list of out of inventory / low items
    # Call the function here
    # Loop over the items
    # Add the forecast for each
    # After that add it to page_data and we can loop over it in the html. (I'll help with this part)
    # forecast(4,1,0,sku,1,connection)

    return render_template("stock-levels.html", context=page_data)

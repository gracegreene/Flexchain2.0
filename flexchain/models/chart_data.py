from collections import OrderedDict

from forecast import forecast
from .location import get_location_name_by_id


def get_txn_amount(cursor):
    headers = ["Date"]
    data = OrderedDict()
    complete_data = list()
    sql = '''
            SELECT month(transaction.date) as month ,year(transaction.date) as year, location1 as location, sum(amount) as total
            FROM transaction
            WHERE transaction.date > DATE_SUB(curdate(), INTERVAL 12 MONTH)
            GROUP BY month(transaction.date), location1
            ORDER BY year, month, location;'''
    cursor.execute(sql)
    for month, year, location, total in cursor:
        if location not in headers:
            headers.append(location)
        if '{}-{:02d}'.format(year, month) not in data:
            data['{}-{:02d}'.format(year, month)] = list()
        data['{}-{:02d}'.format(year, month)].append({location: total})
    temp = []
    for i, v in enumerate(headers):
        if i == 0:
            temp.append(v)
        else:
            location_name = get_location_name_by_id(cursor, v)
            temp.append(location_name)
    complete_data.append(temp)
    for k, v in data.items():
        temp = [k]
        for z in range(len(headers) - 1):
            temp.append(0)
        for d in v:
            for m, n in d.items():
                temp[m] = n
        complete_data.append(temp)
    return complete_data

def get_forecast_inventory(connection, cursor):
    data = list()
    sql = '''SELECT prod_name as product,p.sku AS SKU, SUM(quantity) AS inventory
            FROM current_inventory
            JOIN product p on current_inventory.sku = p.sku
            GROUP BY p.sku;'''
    cursor.execute(sql)
    for product, inventory in cursor:
        data.append({
            'product':product,
            'forecast':forecast(4,1,0,1,connection),
            'current_inventory':inventory
        })
    return data

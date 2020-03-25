from ..forecast import forecast


def get_txn_amount(cursor):
    amounts = list()
    sql = '''
            SELECT month(transaction.date) as month ,year(transaction.date) as year, location1, sum(amount) as total
            FROM transaction
            WHERE transaction.date > DATE_SUB(curdate(), INTERVAL 12 MONTH)
            GROUP BY month(transaction.date), location1;'''
    cursor.execute(sql)
    for month, _, location, total in cursor:
        amounts.append({
            'month':month,
            'location': location,
            'total': total
        })
    return amounts

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

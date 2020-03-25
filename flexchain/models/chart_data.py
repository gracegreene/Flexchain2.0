




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
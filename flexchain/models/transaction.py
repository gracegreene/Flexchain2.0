class Transaction:
    table_name = "transaction"
    table_fields = ["transaction_id", "type", "reason", "amount", "location1", "location2", "date"]

    def __init__(self, date, total_sale, location):
        self.date = date
        self.amount = total_sale
        self.from_location = location

    def create(self, cursor, type, reason, to_location=None):
        insert_sql = "INSERT INTO " + self.table_name + " (" + ",".join(self.table_fields) + ") VALUES (DEFAULT, %s , %s, %s, %s , %s, %s)"
        cursor.execute(insert_sql, (type, reason, self.amount, self.from_location, to_location, self.date))


class TransactionSKU:
    table_name = "transaction_sku"
    table_fields = ['transaction_sku_id', 'transaction_id', 'sku', 'quantity', 'amount_override']

    def __init__(self, sku, quantity, amount_override=0):
        self.sku = sku
        self.quantity = quantity
        self.amount_override = amount_override

    def create(self, cursor, transaction_id):
        self.transaction_id = transaction_id
        insert_sql = "INSERT INTO " + self.table_name + "(" + ",".join(self.table_fields) + ") VALUES (DEFAULT, %s, %s ,%s , %s)"
        cursor.execute(insert_sql, (transaction_id, self.sku, self.quantity, self.amount_override))

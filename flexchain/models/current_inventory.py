class current_inventory:
    table_name = "current_inventory"
    table_fields = ['current_inventory_id', 'sku', 'quantity', 'location_id']

    def __init__(self, sku, quantity, location_id):
        self.sku = sku
        self.quantity = quantity
        self.location_id = location_id

    def create(self, cursor):
        insert_sql = "INSERT INTO " + self.table_name + "(" + ",".join(
            self.table_fields) + ") VALUES (DEFAULT, %s ,%s , %s)"
        cursor.execute(insert_sql, (self.sku, self.quantity, self.location_id))

    def deplete(self, cursor):
        deplete_sql = "UPDATE " + self.table_name + " SET quantity = quantity - %s WHERE sku = %s AND location_id = %s"
        print(deplete_sql % (self.quantity, self.sku, self.location_id))
        cursor.execute(deplete_sql, (self.quantity, self.sku, self.location_id))

    def transfer(self ,cursor, quantity, sku, from_location_id, to_location_id):
        self.deplete(cursor,quantity,sku,from_location_id)
        transfer_sql = "UPDATE " + self.table_name + " SET quantity = quantity + %s WHERE sku = %s AND from location_id = %s"
        cursor.execute(transfer_sql, (quantity, sku, to_location_id))

    def replenish(self, cursor, quantity, sku, location_id):
        replenish_sql = "UPDATE " + self.table_name + " SET quantity = quantity + %s WHERE sku = %s AND location_id = %s"
        cursor.execute(replenish_sql, (quantity, sku, location_id))





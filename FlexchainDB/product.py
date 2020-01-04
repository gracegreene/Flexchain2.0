import mysql.connector

class product:
    def __init__(self,sku,prod_name,description,retail_price, unit_cost, weight, company_code, length=None, width=None,
                 height=None,case_size=None,wholesale_price=None,image_path=None, collection=None):
        self.sku = sku
        self.prod_name = prod_name
        self.description = description
        self.unit_cost = unit_cost
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height
        self.case_size = case_size
        self.wholesale_price = wholesale_price
        self.retail_price = retail_price
        if image_path is None:
            self.image_path = ""
        else:
            self.image_path = image_path
        if collection is None:
            self.collection = ""
        else:
            self.collection = collection
        self.company_code = ""

    def myfunc(self):
        print("This is the product " + self.sku)
        
    def insert_statement_and_data(self):
        insert_product_sql = (
            "INSERT INTO product"
            "(sku, prod_name, description, unit_cost, weight, length, width, height, case_size, wholesale_price, retail_price, image_path, collection, company_code)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        data = (self.sku, self.prod_name, self.description, self.unit_cost, self.weight, self.length, self.width,
                self.height, self.case_size, self.wholesale_price, self.retail_price, self.image_path, self.collection,
                self.company_code)
        return insert_product_sql, data


if __name__ == "__main__":
    connection = mysql.connector.connect(
        host="flexchain-db.c9c4zw0dc4zn.us-east-2.rds.amazonaws.com",
        port=3306,
        user="admin",
        password='w0BtB6lVyAnqG2zMg4R5',
        database='innodb'
    )
    products = list()
    p1= product("7", "product7", "description", 23.13, 1, 12, "cc")
    p2= product("8", "product8", "descirption", 14.21, 1, 12, "cc")
    products.append(p1)
    products.append(p2)
    cursor = connection.cursor()
    try:
        for p in products:
            sql, data = p.insert_statement_and_data()
            cursor.execute(sql, data)
    except Exception as e:
        print(e)
        cursor.close()
        connection.close()

    connection.commit()
    cursor.close()
    connection.close()

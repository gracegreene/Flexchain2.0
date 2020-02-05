import mysql.connector


class product:
    def __init__(self,sku,prod_name,description,retail_price, unit_cost, weight, company_code, length=None, width=None,
                 height=None,case_size=None,wholesale_price=None, collection=None, image_path=None, archive=False):
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
        self.company_code = company_code
        self.archive = archive
        if collection is None:
            self.collection = ""
        else:
            self.collection = collection
        if company_code is None:
            self.company_code = ""
        else:
            self.company_code = company_code
        if image_path is None:
            self.image_path = ""
        else:
            self.image_path = image_path

    def update(self, cursor):
        update_product_sql = '''
        UPDATE product
        SET prod_name=%s, description=%s, unit_cost=%s, weight=%s, length=%s, width=%s, height=%s,
        case_size=%s, wholesale_price=%s, retail_price=%s, collection=%s, company_code=%s, image_path=%s, archive=%s
        WHERE sku =%s
        '''
        data = (self.prod_name, self.description, self.unit_cost, self.weight, self.length, self.width, self.height,
                self.case_size, self.wholesale_price, self.retail_price, self.collection, self.company_code,
                self.image_path, self.archive, self.sku)
        cursor.execute(update_product_sql, data)
        
    def insert_statement_and_data(self):
        insert_product_sql = (
            "INSERT INTO product"
            "(sku, prod_name, description, unit_cost, weight, length, width, height, case_size, wholesale_price, retail_price, collection, company_code, image_path)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        data = (self.sku, self.prod_name, self.description, self.unit_cost, self.weight, self.length, self.width,
                self.height, self.case_size, self.wholesale_price, self.retail_price, self.collection,
                self.company_code, self.image_path)
        return insert_product_sql, data


def get_single_product(cursor, query):
    select_product_sql = '''
    SELECT sku, prod_name, description, unit_cost, weight, length, width, height, case_size, wholesale_price, retail_price, collection, company_code, image_path
    FROM product
    WHERE sku = %s
    LIMIT 1
    '''
    cursor.execute(select_product_sql, (query,))
    for (sku, prod_name, description, unit_cost, weight, length, width, height, case_size, wholesale_price, retail_price, collection, company_code, image_path) in cursor:
        p = product(sku, prod_name, description, retail_price, unit_cost, weight, company_code)
        p.length = length
        p.height = height
        p.case_size = case_size
        p.wholesale_price = wholesale_price
        p.collection = collection
        p.image_path = image_path
        return p


def get_all_products(cursor):
    product_collection = list()
    select_product_sql = '''
    SELECT sku, prod_name, description, image_path, weight
    FROM product
    WHERE archive = false
    ORDER BY prod_name
    '''
    cursor.execute(select_product_sql)
    for (sku, prod_name, description, image_path, weight) in cursor:
        product_collection.append({
            "sku": sku,
            "product_name": prod_name,
            "description": description,
            "image_path": image_path,
            "weight": weight
        })
    return product_collection


def get_product(cursor, query, archive=False):
    product_collection = list()
    select_product_sql = '''
    SELECT sku, prod_name, description, image_path, weight, archive
    FROM product
    WHERE sku = %s
    AND archive = %s
    OR prod_name like CONCAT("%", %s, "%")
    AND archive = %s
    '''
    cursor.execute(select_product_sql, (query, archive, query.lower(), archive))
    for (sku, prod_name, description, image_path, weight, archive) in cursor:
        product_collection.append({
            "sku": sku,
            "product_name": prod_name,
            "description": description,
            "image_path": image_path,
            "weight": weight,
            "archive": archive,
        })
    return product_collection


if __name__ == "__main__":
    connection = mysql.connector.connect(
        host="flexchain-db.c9c4zw0dc4zn.us-east-2.rds.amazonaws.com",
        port=3306,
        user="admin",
        password='w0BtB6lVyAnqG2zMg4R5',
        database='innodb'
    )
    cursor = connection.cursor()
    try:
        for product in get_product(cursor, "NEWSK"):
            print(product["sku"])
            print(product["product_name"])
            print(product["description"])
            print(product["image_path"])
    except Exception as e:
        print(e)
        cursor.close()
        connection.close()

    connection.commit()
    cursor.close()
    connection.close()

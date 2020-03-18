from datetime import datetime, timedelta

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


def get_product(cursor, sku, archive=False):
    product_collection = list()
    select_product_sql = '''
    SELECT sku, prod_name, description, image_path, weight, archive
    FROM product
    WHERE sku = %s
    AND archive = %s
    OR prod_name like CONCAT("%", %s, "%")
    AND archive = %s
    '''
    cursor.execute(select_product_sql, (sku, archive, query.lower(), archive))
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


def get_ROP(sku):
    return 1000
    #R= NORMSINV(service level) x Standard Dev of demand for SKU
    z = norm.ppf(0.95, loc=10, scale=2)

    sql = '''select STR_TO_DATE(concat_ws("-",month(transaction.date),year(transaction.date),"01"), "%m-%Y-%d") as monthofsale,sum(quantity)
                    from transaction join transaction_sku on transaction.transaction_id = transaction_sku.transaction_id
                    join product on transaction_sku.sku = product.sku
                    where product.sku='{}'
                    and transaction.reason = 'Sale'
                    group by monthofsale,prod_name
                    order by transaction.date;
    '''.format(sku)
    series = read_sql(sql, con=connection, parse_dates=0, index_col=["monthofsale"])
    sales = series.values
    sigma = np.std(sales)
    return z*sigma

def get_product_low(cursor):
    product_collection = list()
    ROP_temp_list = list()
    skus = list()

    select_allsku_sql = '''        
                SELECT sku from product;        
                '''

    cursor.execute(select_allsku_sql)
    for sku in cursor:
        skus.append(sku[0])

    for sku in skus:
        rop = get_ROP(sku)

        select_product_sql = '''        
                SELECT product, name, image, total_inventory FROM
                    (select current_inventory.sku as product, p.prod_name as name,p.image_path as image, sum(quantity) as total_inventory
                        from location join current_inventory on location.location_id = current_inventory.location_id
                        join product p on current_inventory.sku = p.sku
                        group by p.sku) as inventory
                WHERE total_inventory < %s 
                AND product = %s;        
                '''
        cursor.execute(select_product_sql, (rop, sku))
        for s, name, image, unused in cursor:
            product_collection.append({
                "sku": s,
                "product_name": name,
                "image_path": image,
                "alert": "CRITICAL LEVEL"
            })

    return product_collection


def get_product_out(cursor):
    product_collection = list()
    select_product_sql = '''        
        SELECT sku,name,image FROM
            (select current_inventory.sku as sku,p.prod_name as name,p.image_path as image, sum(quantity) as total_inventory
                from location join current_inventory on location.location_id = current_inventory.location_id
                join product p on current_inventory.sku = p.sku
                group by p.sku) as inventory
        WHERE inventory.total_inventory < 1;        
        '''
    cursor.execute(select_product_sql)
    for sku, name, image in cursor:
        product_collection.append({
            "sku": sku,
            "product_name": name,
            "image_path": image,
            "alert": "Out of Inventory"
        })
    return product_collection

def get_itr(cursor):
    itr_by_location = list()
    sql = '''SELECT DISTINCT sales.sku, sales.location, 2*(sales.unit_cost*sales.sum)/(end_inventory.quantity+start_inventory.quantity) AS ITR FROM (SELECT sku, quantity, location_id FROM inventory
            WHERE month = month(curdate())-1
            AND year = year(curdate())-1) AS start_inventory
            JOIN (select sku, quantity, location_id from inventory
            where month = month(curdate())-1 and year = year(curdate())) AS end_inventory
            ON start_inventory.sku=end_inventory.sku AND start_inventory.location_id=end_inventory.location_id
            JOIN (SELECT sales.*, product.unit_cost FROM (SELECT product.sku, transaction.location1 AS location, sum(quantity) AS sum
                                    FROM transaction JOIN transaction_sku ON transaction.transaction_id = transaction_sku.transaction_id
                                    JOIN product ON transaction_sku.sku = product.sku
                                    AND transaction.reason = 'sale'
            AND transaction.date < date_add(date_add(LAST_DAY(CURDATE()),interval 1 DAY),interval -2 MONTH)
            AND transaction.date > date_add(date_add(date_add(LAST_DAY(CURDATE()),interval 1 DAY),interval -2 MONTH), interval -1 YEAR)
            GROUP BY location1, product.sku) AS sales JOIN product on sales.sku = product.sku) AS sales
            ON sales.sku=start_inventory.sku AND sales.location=start_inventory.location_id
            ORDER BY ITR DESC;'''
    cursor.execute(sql)
    for (sku, location, itr) in cursor:
        itr_by_location.append({
            'sku': sku,
            'location': location,
            'itr': itr
        })
    return itr_by_location

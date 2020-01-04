import mysql.connector


class location:
    def __init__(self, location_id,location_type,loc_name,country,state,street_address,zipcode,
                 integration_id=None, coordinates=None, notes=None, company_code=None):
        self.location_id = location_id
        self.location_type = location_type
        self.loc_name = loc_name
        self.country = country
        self.state = state
        self.street_address = street_address
        self.zipcode = zipcode
        if integration_id is None:
            self.integration_id = ""
        else:
            self.integration_id = integration_id
        if coordinates is None:
            self.coordinates = ""
        else:
            self.coordinates = coordinates
        if notes is None:
            self.notes = ""
        else:
            self.notes = notes
        if company_code is None:
            self.company_code = ""
        else:
            self.company_code = company_code

    def insert_statement_and_data(self):
        insert_location_sql = (
            "INSERT INTO location"
            "(location_id, location_type, loc_name, country, state, street_address, zipcode, integration_id, coordinates, notes,company_code)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        data = (self.location_id, self.location_type, self.loc_name, self.country, self.state, self.street_address, self.zipcode,
                self.integration_id, self.coordinates, self.notes,self.company_code)
        return insert_product_sql, data


if __name__ == "__main__":
    connection = mysql.connector.connect(
        host="flexchain-db.c9c4zw0dc4zn.us-east-2.rds.amazonaws.com",
        port=3306,
        user="admin",
        password='w0BtB6lVyAnqG2zMg4R5',
        database='innodb'
    )
    locations = list()
    p1 = product("7", "product7", "loc_name", 23.13, 1, 12, "cc")
    p2 = product("8", "product8", "descirption", 14.21, 1, 12, "cc")
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

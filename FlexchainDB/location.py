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
        return insert_location_sql, data

def get_location(cursor, query):
    location_collection = list()
    select_location_sql  = '''
    SELECT location_id, loc_name, location_type, state, zipcode
    FROM location
    WHERE location_id = %s
    OR loc_name like %s
    '''
    cursor.execute(select_location_sql, (query, query))
    for (location_id, loc_name, location_type, state, zipcode) in cursor:
        location_collection.append({
            "location_id": location_id,
            "loc_name": loc_name,
            "location_type": location_type,
            "state": state,
            "zipcode": zipcode
        })
    return location_collection




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
        for location in get_location(cursor, "NEWSK"):
            print(location["location_id"])
            print(location["loc_name"])
            print(location["location_type"])
            print(location["state"])
    except Exception as e:
        print(e)
        cursor.close()
        connection.close()

    connection.commit()
    cursor.close()
    connection.close()
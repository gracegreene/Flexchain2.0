class location:
    def __init__(self, location_id, location_type, loc_name, country, state, street_address, zipcode,
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

    def insert(self, cursor):
        insert_location_sql = (
            "INSERT INTO location"
            "(location_id, location_type, loc_name, country, state, street_address, zipcode, integration_id, coordinates, notes,company_code)"
            "VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        data = (self.location_type, self.loc_name, self.country, self.state, self.street_address, self.zipcode,
                self.integration_id, self.coordinates, self.notes, self.company_code)
        cursor.execute(insert_location_sql, data)
        return


def get_locations(cursor, query):
    location_collection = list()
    select_location_sql = '''
        SELECT location_id, loc_name, state, zipcode, coordinates
        FROM location
        WHERE location_type=%s
        '''
    cursor.execute(select_location_sql, (query,))
    for (location_id, loc_name, state, zipcode, coordinates) in cursor:
        location_collection.append({
            "location_id": location_id,
            "loc_name": loc_name,
            "state": state,
            "zipcode": zipcode,
            "coordinates": coordinates,
        })
    return location_collection


def get_all_locations(cursor):
    location_collection = list()
    select_location_sql = '''
        SELECT location_id, loc_name, state, zipcode, coordinates
        FROM location
        ORDER BY loc_name
        '''
    cursor.execute(select_location_sql)
    for (location_id, loc_name, state, zipcode, coordinates) in cursor:
        location_collection.append({
            "location_id": location_id,
            "loc_name": loc_name,
            "state": state,
            "zipcode": zipcode,
            "coordinates": coordinates,
        })
    return location_collection


def get_store(cursor):
    return get_locations(cursor, "store")


def get_warehouse(cursor):
    return get_locations(cursor, "warehouse")


def get_customer(cursor):
    return get_locations(cursor, "customer")

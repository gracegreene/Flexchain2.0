def get_last_insert_id(cursor):
    cursor.execute("SELECT LAST_INSERT_ID()")
    for id in cursor:
        return id
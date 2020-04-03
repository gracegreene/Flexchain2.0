def login_user(cursor, email, password):
    name = None
    sql = '''SELECT first_name FROM user WHERE email = %s AND password = %s'''
    cursor.execute(sql, (email, password))
    for first_name in cursor:
        name = first_name[0]
    return name

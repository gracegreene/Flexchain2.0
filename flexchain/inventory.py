from datetime import datetime

import click
from flask.cli import with_appcontext

from .db import get_db


def monthdelta(date, delta):
    m, y = (date.month + delta) % 12, date.year + ((date.month) + delta - 1) // 12
    if not m: m = 12
    d = min(date.day, [31,
                       29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    return date.replace(day=d, month=m, year=y)


@click.command('monthly-cron-inventory')
@with_appcontext
def monthly_cron_inventory():
    today = datetime.now()
    this_month_date = datetime(today.year, today.month, 1)
    last_month_date = monthdelta(this_month_date, -1)  # Subtract a month of time away.
    print(last_month_date.year, "-", last_month_date.month)
    try:
        inventory = list()
        connection = get_db()
        cursor = connection.cursor()
        get_inventory_sql = '''
        SELECT sku, quantity, location_id
        FROM current_inventory
        '''
        insert_inventory_sql = '''
        INSERT INTO inventory VALUES (DEFAULT, %s, %s, %s, %s, %s)
        '''
        cursor.execute(get_inventory_sql)
        for (sku, quantity, location_id) in cursor:
            inventory.append(
                (sku, last_month_date.month, last_month_date.year, quantity, location_id)
            )
        cursor.executemany(insert_inventory_sql, inventory)
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(e)
    click.echo("Completed monthly cron job")


def init_app(app):
    # app.teardown_appcontext(close_db)
    app.cli.add_command(monthly_cron_inventory)

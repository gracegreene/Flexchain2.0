import mysql.connector
from pandas import read_sql
from matplotlib import pyplot
from pandas import DataFrame
from statsmodels.tsa.arima_model import ARIMA
from pandas.plotting import autocorrelation_plot
from datetime import datetime
from sklearn.metrics import mean_squared_error


def parser(x):
    return datetime.strptime(x, '%Y-%m-%d')


def forecast(p,q,d,sku,next_forecast,connection):
    predictions = list()

    try:
        sql = '''select STR_TO_DATE(concat_ws("-",month(transaction.date),year(transaction.date),"01"), "%m-%Y-%d") as monthofsale,sum(quantity)
                        from transaction join transaction_sku on transaction.transaction_id = transaction_sku.transaction_id
                        join product on transaction_sku.sku = product.sku
                        where product.sku='{}'
                        and transaction.reason = 'Sale'
                        group by monthofsale,prod_name
                        order by transaction.date;
        '''.format(sku)
        series = read_sql(sql, con=connection, parse_dates=0, index_col=["monthofsale"])
        # fit model
        sales = series.values
        history = [x for x in sales]
        for t in range(next_forecast):
            model = ARIMA(history, order=(p, d, q))
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            yhat = output[0]
            predictions.append(yhat)
            history.append(yhat)
    except Exception as e:
        print(e)
    return predictions


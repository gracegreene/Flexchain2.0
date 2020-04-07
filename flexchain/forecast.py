from pandas import read_sql
from statsmodels.tsa.arima_model import ARIMA
from datetime import datetime


def parser(x):
    return datetime.strptime(x, '%Y-%m-%d')


def forecast(p, q, d, sku, next_forecast, connection):
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
            if len(yhat) != 0:
                predictions.append(yhat[0])
            history.append(yhat)
    except Exception as e:
        print(e)
    print(predictions)
    return predictions


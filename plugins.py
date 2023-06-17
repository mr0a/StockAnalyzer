import datetime
from stock_analyzer.IndicatorPlugin import IndicatorPlugin
import pandas as pd
import talib


class MovingAveragePlugin(IndicatorPlugin):
    def calculate(self, data):
        # Perform moving average calculation on data
        # Return the calculated result
        return "Moving Average: {}".format(data)


class RSIPlugin(IndicatorPlugin):
    def calculate(self, data):
        # Perform RSI calculation on data
        # Return the calculated result
        return "RSI: {}".format(data)


class CPR(IndicatorPlugin):
    def calculate(self, data):
        df = pd.DataFrame(data)
        df = df.drop(['stat', 'oi', 'intoi'], axis=1)
        df['time'] = pd.to_datetime(df['time'], format='%d-%m-%Y %H:%M:%S')
        todayStart = datetime.datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0)
        yesterday = todayStart - datetime.timedelta(days=1)
        dt_range = pd.date_range(start=yesterday, end=todayStart, freq='T')
        df1 = df[df['time'].isin(dt_range)]
        open = float(df1.iloc[-1]['into'])
        low = float(df1['intl'].min())
        high = float(df1['inth'].max())
        close = float(df1.iloc[0]['intc'])

        central_cpr = (high + low + close) / 3
        bottom_cpr = (high + low) / 2
        top_cpr = (central_cpr - bottom_cpr) + central_cpr
        # bottom_cpr = 2 * central_cpr - high
        # top_cpr = 2 * central_cpr - low

        print(f'Shelbot\U0001F60E: Calculating Pivot Values... with',
              open, low, high, close)

        return {
            "pivot": {
                "center": central_cpr,
                "tc": top_cpr,
                "bc": bottom_cpr
            },
            'narrowCPR': (2 * abs(central_cpr - bottom_cpr) < 0.005 * close)
        }


class EMA(IndicatorPlugin):
    def calculate(self, data):
        df = pd.DataFrame(data)[::-1]
        df['intc'] = pd.to_numeric(df['intc'])
        return talib.EMA(df['intc'], timeperiod=67)

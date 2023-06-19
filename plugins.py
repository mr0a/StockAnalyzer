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
        if not (data or len(data)):
            print("No data available to calculate CPR")
            return False
        df = pd.DataFrame(data)
        df = df.drop(['stat', 'oi', 'intoi'], axis=1)
        df['time'] = pd.to_datetime(df['time'], format='%d-%m-%Y %H:%M:%S')
        previousTradingDayStart = df.iloc[0]['time'].replace(hour=9, minute=15)
        previousTradingDayEnd = df.iloc[0]['time'].replace(hour=15, minute=30)
        # Code to calculate cpr for friday
        # previousTradingDayEnd = previousTradingDayEnd - \
        #     datetime.timedelta(days=1)
        # previousTradingDayStart = previousTradingDayStart - \
        #     datetime.timedelta(days=1)
        dt_range = pd.date_range(
            start=previousTradingDayStart, end=previousTradingDayEnd, freq='T')
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
              open, high, low, close)

        return {
            "pivot": {
                "pivot": central_cpr,
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

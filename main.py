import asyncio
from getData import get_time_price_data
from plugins import CPR, EMA
from stock_analyzer.StockAnalyzer import StockAnalyzer


async def main():

    stockName = input("Enter Stock Name: ")
    data = await get_time_price_data(stockName)
    ema_and_narrow_cpr_analyzer = StockAnalyzer()
    ema_and_narrow_cpr_analyzer.register_plugin(EMA())
    ema_and_narrow_cpr_analyzer.register_plugin(CPR())
    ema_and_narrow_cpr_analyzer.analyze(data)


asyncio.run(main())

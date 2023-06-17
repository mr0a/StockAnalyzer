import json
import pprint
import aiohttp
import asyncio
import datetime


access_token = '81cfb6eaf761a14094c7ccc6fb1e299a2a4348a9b17120c5e53b87bba64cd18c'
BASE_URL = 'https://piconnect.flattrade.in/PiConnectTP'
client_id = 'FT013065'

# query = input("Enter the stock Name: ")


async def search_scrips(query, exchange):
    async with aiohttp.ClientSession() as session:
        jData = {
            "uid": client_id,
            "stext": query,
            "exch": 'NSE'
        }
        json_jdata = json.dumps(jData)
        data = f"jData={json_jdata}&jKey={access_token}"
        response = await session.post(BASE_URL + "/SearchScrip", data=data)
        # pprint.pprint(await response.json())
        json_response = await response.json()
        return json_response.get("values")


async def get_time_price_data(symbol,
                              start_time=(datetime.datetime.now(
                              )-datetime.timedelta(days=100)).timestamp(),
                              end_time=datetime.datetime.now().timestamp(),
                              interval="60"):
    searchResults = await search_scrips(symbol, 'NSE')
    if len(searchResults) == 0:
        print("No stock found in such name")

    stock = searchResults[0]
    async with aiohttp.ClientSession() as session:
        jData = {
            "uid": client_id,
            "exch": 'NSE',
            "token": stock.get('token'),
            "st": str(start_time),
            "et": str(end_time),
            "intrv": interval
        }
        json_jdata = json.dumps(jData)
        data = f"jData={json_jdata}&jKey={access_token}"
        response = await session.post(BASE_URL + "/TPSeries", data=data)
        content = await response.content.read()
        decoded = content.decode('utf-8')
        json_response = json.loads(decoded)
        # pprint.pprint(json_response)
        return json_response


async def get_eod_data(symbol,
                       start_time=(datetime.datetime.now() -
                                   datetime.timedelta(days=100)).timestamp(),
                       end_time=datetime.datetime.now().timestamp()):
    searchResults = await search_scrips(symbol, 'NSE')
    if len(searchResults) == 0:
        print("No stock found in such name")

    stock = searchResults[0]
    async with aiohttp.ClientSession() as session:
        jData = {
            # "uid": client_id,
            # "exch": 'NSE',
            # "token": stock.get('token'),
            "sym": f"{stock.get('exch')}:{stock.get('tsym')}",
            "from": str(start_time),
            "to": str(end_time)
        }
        json_jdata = json.dumps(jData)
        data = f"jData={json_jdata}&jKey={access_token}"
        response = await session.post(BASE_URL + "/EODChartData", data=data)
        content = await response.content.read()
        decoded = content.decode('utf-8')
        json_response = json.loads(decoded)
        return json_response


# get_time_price_data(query)
# asyncio.run(get_time_price_data(query))

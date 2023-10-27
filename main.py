import asyncio
import logging
import argparse
import json
import sys

import websockets
import names
import aiohttp
from datetime import datetime, date ,timedelta
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from aiofile import async_open


###########  Ввідні дані  #############

parser = argparse.ArgumentParser(description="exchange")
parser.add_argument("--previous_days", "-p", help="previous_days", default=1)
parser.add_argument("--currency", "-c", help="currency", default=['EUR','USD'])
parser.add_argument("--web_server", "-w", help="web_server", default=None)

args = vars(parser.parse_args())

previous_days = int(args.get("previous_days"))
currencies = args.get("currency")
web_server = args.get("web_server")
date_now = date.today()

api_privat = "https://api.privatbank.ua/p24api/exchange_rates?date="

result_api = []
logging.basicConfig(level=logging.INFO)

file_name = "log.txt"

##############  Клієнт aiohttp  ###############

async def request(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                r = await response.json()
                return r
            else:
                return "Error.Приват не відповідає"
#json.dump(json_dict, f, ensure_ascii=False, indent=4)

##############  Парсер API запитів  ###############
async def parser_api(response,day):
    d2 = {}
    for i in response["exchangeRate"]:
        if i.get('currency') in  currencies:
            d1 = {'sale': i.get('saleRateNB'), 'purchase': i.get('purchaseRateNB')}
            d2.update({i.get('currency'): d1})        
    return d2

##############  Функція для виконання API запитів  ###############
async def get_exchange():
    for day in range(previous_days):
        day = timedelta(days = day)
        date_exchange = date_now - day
        date_exchange = date_exchange.strftime('%d.%m.%Y')
        response = await request(f"{api_privat}{date_exchange}")
        result =  await parser_api(response, day) 
        dict_date = {response["date"]: result} 
        result_api.append(dict_date)
    return str(result_api)


async def log(message):
    async with async_open("log.txt", 'w+') as afp:
        await afp.write(message)


###############  Web cервер  ######################### 
class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message == "exchange":
                exchange = await get_exchange()
                print(exchange)
                await self.send_to_clients(exchange)
            elif message == "Hello server":
                await self.send_to_clients("Hello")
            await self.send_to_clients(f"{ws.name}: {message}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    
#############  приклад запуску з командної строки   ################
############# python main.py -p 2 -c CHF,EUR -w run <<<    ################
    if web_server == "run":
        asyncio.run(main())
        asyncio.run(log("odpjgiojernhbg"))


    if 1 <= previous_days <= 10:
        print(F"Виконується запит курсу валют {currencies}")
        asyncio.run(get_exchange())
        
        print(json.dumps(result_api, ensure_ascii=False, indent=4))
    else:
        print("Введіть кількість днів для запиту від '1' до '10' ")
      


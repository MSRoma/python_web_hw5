import asyncio
import logging
import argparse

import websockets
import names
import aiohttp
from datetime import datetime, date ,timedelta
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK



parser = argparse.ArgumentParser(description="exchange")
parser.add_argument("--exchange", "-ex", help="exchange", default=1)
args = vars(parser.parse_args())
day_ = int(args.get("exchange"))
date_now = date.today()

logging.basicConfig(level=logging.INFO)

async def request(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                list_pb = []
                dict_pb = {}
                key = []
                r = await response.json()
                result = r#.json()
                key.append(result["date"])
                for i in result["exchangeRate"]:
                    
                        print(i)
                
                return print(key)
            else:
                return "Error.Приват не відповідає"
#json.dump(json_dict, f, ensure_ascii=False, indent=4)

async def get_exchange():
    for i in range(day_):
        i = timedelta(days=i)
        d = date_now - i
        dt_now = d.strftime('%d.%m.%Y')
        response = await request(f"https://api.privatbank.ua/p24api/exchange_rates?date={dt_now}")


    #    return str(response) 

# class Server:
#     clients = set()

#     async def register(self, ws: WebSocketServerProtocol):
#         ws.name = names.get_full_name()
#         self.clients.add(ws)
#         logging.info(f'{ws.remote_address} connects')

#     async def unregister(self, ws: WebSocketServerProtocol):
#         self.clients.remove(ws)
#         logging.info(f'{ws.remote_address} disconnects')

#     async def send_to_clients(self, message: str):
#         if self.clients:
#             [await client.send(message) for client in self.clients]

#     async def ws_handler(self, ws: WebSocketServerProtocol):
#         await self.register(ws)
#         try:
#             await self.distrubute(ws)
#         except ConnectionClosedOK:
#             pass
#         finally:
#             await self.unregister(ws)

#     async def distrubute(self, ws: WebSocketServerProtocol):
#         async for message in ws:
#             if message == "exchange":
#                 exchange = await get_exchange()
#                 print(exchange)
#                 await self.send_to_clients(exchange)
#             elif message == "Hello server":
#                 await self.send_to_clients("Hello")
#             await self.send_to_clients(f"{ws.name}: {message}")


# async def main():
#     server = Server()
#     async with websockets.serve(server.ws_handler, 'localhost', 8080):
#         await asyncio.Future()  # run forever

if __name__ == '__main__':
    
         #   asyncio.run(main())

        asyncio.run(get_exchange())


 
import asyncio,datetime
import websockets
import time, json
from  bot import Bot

connected = set()

async def server(websocket, path):
    # Register.
    connected.add(websocket)
    bot_ = Bot()
    bot_.get_local_driver()
    bot_.work()
    try:
        while True:
            for conn in connected:
                main_data = await bot_.return_main_data_for_all_windows_parallel()
                await conn.send(json.dumps({"data": main_data}))
                print(f'\n\n\n Dattime : {datetime.datetime.now()}')
    finally:
        # Unregister.
        connected.remove(websocket)

start_server = websockets.serve(server, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

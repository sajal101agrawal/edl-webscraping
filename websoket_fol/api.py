import asyncio
import websockets
import json, datetime
from bot import Bot

# Initialize bot

connected = set()
bot_ = Bot()
bot_.get_local_driver()
bot_.work()


async def echo(websocket, path):
    connected.add(websocket)
    while True:
        if connected:
            main_data = await bot_.return_main_data_for_all_windows_parallel()
            for conn in connected:
                await conn.send(json.dumps({"data": main_data}))
    connected.remove(websocket)

start_server = websockets.serve(echo, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

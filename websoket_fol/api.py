import asyncio
import websockets
import json, datetime
from bot import Bot
import time
# Initialize bot
print(__name__)
connected = set()
bot_ = Bot()
bot_.get_local_driver()
bot_.work()


connected = set()
time.sleep(10)
print('websocket start')
async def echo(websocket, path):
    connected.add(websocket)
    try:
        while True:
            main_data = await bot_.return_main_data_for_all_windows_parallel()
            await websocket.send(json.dumps({"data": main_data}))  
    except:pass  
    finally:
        connected.remove(websocket)

start_server = websockets.serve(echo, "0.0.0.0", 8765)


asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
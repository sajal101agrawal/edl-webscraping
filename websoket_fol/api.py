import asyncio
import websockets
import json
from bot import Bot
import time

# Initialize bot
if __name__ == '__main__':
    connected = set()
    bot_ = Bot()
    bot_.get_driver()
    while not bot_.work(): 
        pass

    time.sleep(10)
    print('websocket start')

    async def echo(websocket, path):
        connected.add(websocket)
        try:
            while True:
                main_data = await bot_.return_main_data_for_all_windows_parallel()
                await websocket.send(json.dumps({"data": main_data}))
                await asyncio.sleep(1)  # Send data every second (adjust as needed)
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed with error: {e}")
        except websockets.exceptions.ConnectionClosedOK:
            print("Connection closed normally")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            connected.remove(websocket)

    async def ping():
        while True:
            for ws in connected:
                try:
                    await ws.ping()
                except Exception as e:
                    print(f"Ping error: {e}")
            await asyncio.sleep(1)  # Ping every 10 seconds (adjust as needed)

    start_server = websockets.serve(echo, "0.0.0.0", 8765)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.create_task(ping())
    loop.run_forever()
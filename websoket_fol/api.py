import os
import time
import json
import signal
import asyncio
import websockets
import subprocess
from bot import Bot


def kill_chrome_drivers():
    try:
        # Attempt to kill all ChromeDriver processes
        result = subprocess.run(['pkill', '-f', 'chromedriver'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            print("All ChromeDriver processes have been terminated.")
        elif "Operation not permitted" in result.stderr:
            print("Permission denied. Please run the script with elevated privileges (e.g., using sudo).")
        else:
            print(f"No ChromeDriver processes found or an error occurred: {result.stderr.strip()}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Initialize bot
if __name__ == '__main__':
    while True:
        try:
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
                except websockets.exceptions.ConnectionClosedError as e:
                    print(f"Connection closed with error: {e}")
                except websockets.exceptions.ConnectionClosedOK:
                    print("Connection closed normally")
                except asyncio.CancelledError:
                    print("Connection cancelled")
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
        except Exception as e :
            kill_chrome_drivers()

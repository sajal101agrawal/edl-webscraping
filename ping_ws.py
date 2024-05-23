import asyncio
import websockets
import subprocess
import os

async def ping_server():
    uri = "ws://0.0.0.0:8765"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    try:
                        await websocket.ping()
                        print("Ping sent successfully")
                    except websockets.exceptions.ConnectionClosed as e:
                        print(f"Connection closed: {e}")
                        break
                    except Exception as e:
                        print(f"Error occurred: {e}")
                        # Kill the process
                        subprocess.run(["pkill", "-f", "start.sh"])
                        # Restart the process
                        subprocess.Popen(["nohup", "./start.sh", ">", "/home/DickiData/edl-webscraping/server.log", "2>&1", "&"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        break
                    await asyncio.sleep(10)  # Ping every 10 seconds
        except Exception as e:
            print(f"Error occurred while connecting to the WebSocket server: {e}")
            break

asyncio.get_event_loop().run_until_complete(ping_server())

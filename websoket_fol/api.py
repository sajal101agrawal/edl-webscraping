import time
import json
import asyncio
import websockets
import subprocess
from websoket_fol.bot import Bot
import logging

logging.basicConfig(filename='api.log',level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

import psutil

def kill_port(port):
    try:
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            for conn in proc.info['connections']:
                if conn.laddr.port == port:
                    print(f"Killing process {proc.pid} ({proc.name()}) using port {port}...")
                    proc.kill()
                    print("Process killed.")
                    return
        print(f"No process found using port {port}.")
    except Exception as e:
        logging.info(f'When kill port script found this error: {e}')

def kill_chrome_drivers():
    try:
        # Attempt to kill all ChromeDriver processes
        result = subprocess.run(['pkill', '-f', 'chromedriver'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            logging.info("All ChromeDriver processes have been terminated.")
        elif "Operation not permitted" in result.stderr:
            logging.info("Permission denied. Please run the script with elevated privileges (e.g., using sudo).")
        else:
            logging.info(f"No ChromeDriver processes found or an error occurred: {result.stderr.strip()}")
    except Exception as e:
        logging.info(f"An error occurred: {e}")

# Initialize bot
if __name__ == '__main__':
    while True:
        try:
            kill_port(8765)
            while True:
                connected = set()
                bot_ = Bot()
                bot_.get_driver()
                bot_.work()
                    

                time.sleep(10)
                logging.info('websocket start')

                async def echo(websocket, path):
                    connected.add(websocket)
                    try:
                        while True:
                            main_data = await bot_.return_main_data_for_all_windows_parallel()
                            await websocket.send(json.dumps({"data": main_data}))
                    except websockets.exceptions.ConnectionClosedError as e:
                        logging.info(f"Connection closed with error: {e}")
                    except websockets.exceptions.ConnectionClosedOK:
                        logging.info("Connection closed normally")
                    except asyncio.CancelledError:
                        logging.info("Connection cancelled")
                    except Exception as e:
                        logging.info(f"Unexpected error: {e}")
                    finally:
                        connected.remove(websocket)

                async def ping():
                    while True:
                        for ws in connected:
                            try:
                                await ws.ping()
                            except Exception as e:
                                logging.info(f"Ping error: {e}")
                        await asyncio.sleep(1)  # Ping every 10 seconds (adjust as needed)

                start_server = websockets.serve(echo, "0.0.0.0", 8765)
                loop = asyncio.get_event_loop()
                loop.run_until_complete(start_server)
                loop.create_task(ping())
                loop.run_forever()
        except Exception as e :
            logging.info(f"Main error: {e}")
            kill_chrome_drivers()

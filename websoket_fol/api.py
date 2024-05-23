import time
import json
import asyncio
import websockets
import subprocess
from bot import Bot
import logging
import psutil

logging.basicConfig(filename='api.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

async def echo(websocket, path):
    try:
        bot = Bot()
        bot.get_driver()
        while True:
            main_data = await bot.return_main_data_for_all_windows_parallel()
            await websocket.send(json.dumps({"data": main_data}))
    except websockets.exceptions.ConnectionClosedError as e:
        logging.info(f"Connection closed with error: {e}")
    except asyncio.CancelledError:
        logging.info("Connection cancelled")
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")

async def ping(websockets):
    try:
        while True:
            for ws in websockets:
                try:
                    await ws.ping()
                except Exception as e:
                    logging.info(f"Ping error: {e}")
            await asyncio.sleep(10)  # Ping every 10 seconds (adjust as needed)
    except asyncio.CancelledError:
        logging.info("Ping cancelled")
    except Exception as e:
        logging.exception(f"Ping loop error: {e}")

async def serve():
    async with websockets.serve(echo, "0.0.0.0", 8765):
        await asyncio.Future()  # Serve forever

def kill_port(port):
    try:
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            for conn in proc.info['connections']:
                if conn.laddr.port == port:
                    logging.info(f"Killing process {proc.pid} ({proc.name()}) using port {port}...")
                    proc.kill()
                    logging.info("Process killed.")
                    return
        logging.info(f"No process found using port {port}.")
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

if __name__ == '__main__':
    while True:
        kill_port(8765)
        try:
            loop = asyncio.get_event_loop()
            websocket_task = loop.create_task(serve())
            ping_task = loop.create_task(ping(set()))

            loop.run_until_complete(asyncio.gather(websocket_task, ping_task))
        except Exception as e:
            logging.exception(f"Main error: {e}")
            kill_chrome_drivers()

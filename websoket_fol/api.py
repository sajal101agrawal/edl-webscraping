# import time
# import json
# import asyncio
# import websockets
# import subprocess
# from bot import *


# import psutil

# def kill_port(port):
#     try:
#         for proc in psutil.process_iter(['pid', 'name', 'connections']):
#             connections = proc.info.get('connections')
#             if connections:
#                 for conn in connections:
#                     if getattr(conn.laddr, 'port', None) == port:
#                         logging.info(f"Killing process {proc.pid} ({proc.name()}) using port {port}...")
#                         proc.kill()
#                         logging.info("Process killed.")
#                         return True
#         logging.info(f"No process found using port {port}.")
#         return False
#     except Exception as e:
#         logging.info(f'When kill port script found this error: {e}')

# def kill_chrome_drivers():
#     try:
#         # Attempt to kill all ChromeDriver processes
#         result = subprocess.run(['pkill', '-f', 'chromedriver'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

#         if result.returncode == 0:
#             logging.info("All ChromeDriver processes have been terminated.")
#         elif "Operation not permitted" in result.stderr:
#             logging.info("Permission denied. Please run the script with elevated privileges (e.g., using sudo).")
#         else:
#             logging.info(f"No ChromeDriver processes found or an error occurred: {result.stderr.strip()}")
#         result = subprocess.run(['pkill', 'chrome'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         if result.returncode == 0:
#             logging.info("All Chrome processes have been terminated.")
#         elif "No matching processes" in result.stderr:
#             logging.info("No Chrome processes found or an error occurred.")
#         else:
#             logging.info(f"Unknown error occurred: {result.stderr.strip()}")
#     except Exception as e:
#         logging.info(f"An error occurred: {e}")

# # Initialize bot
# if __name__ == '__main__':
#         connected = set()
#         logging.info('websocket start')

#         async def echo(websocket, path):
#             def get_file_modification_time(filepath):
#                 return os.path.getmtime(filepath)
#             filepath  =  'data.json'
#             last_mod_time = get_file_modification_time(filepath)
#             connected.add(websocket)
#             try:
#                 while True:
#                     try:
#                         # current_mod_time = get_file_modification_time(filepath)
#                         # if current_mod_time != last_mod_time:
#                         with open(filepath, 'r') as file:
#                             data = json.load(file)
#                             # print("File has been updated.")
#                             # last_mod_time = current_mod_time
#                         await websocket.send(json.dumps({"data": data}))
#                         time.sleep(1)
#                     except FileNotFoundError:
#                         logging.info(f"File {filepath} not found.")
#                         break
#                     except Exception as e:
#                         logging.info(f"An error occurred: {e}")
#                         break
#             except websockets.exceptions.ConnectionClosedError as e:
#                 logging.info(f"Connection closed with error: {e}")
#             except websockets.exceptions.ConnectionClosedOK:
#                 logging.info("Connection closed normally")
#             except asyncio.CancelledError:
#                 logging.info("Connection cancelled")
#             except Exception as e:
#                 logging.info(f"Unexpected error: {e}")
#             finally:
#                 connected.remove(websocket)

#         async def ping():
#             while True:
#                 for ws in set(connected):  # Create a shallow copy of the connected set
#                     try:
#                         await ws.ping()
#                     except Exception as e:
#                         logging.info(f"Ping error: {e}")
#                 await asyncio.sleep(1)  # Ping every 10 seconds (adjust as needed)

#         start_server = websockets.serve(echo, "0.0.0.0", 8765)
#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(start_server)
#         # loop.create_task(ping())
#         loop.run_forever()



import asyncio
import json
import logging
import os
import psutil
import subprocess
import websockets
import time
from filelock import FileLock

# base_path = os.path.join(os.getcwd(), 'data.json')
base_path = '/home/DickiData/edl-webscraping/websoket_fol/data.json'
if not os.path.isfile(base_path):
    with open(base_path, 'w') as file:
        json.dump({}, file, indent=4)

logging.basicConfig(level=logging.INFO)

def kill_port(port):
    try:
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            connections = proc.info.get('connections')
            if connections:
                for conn in connections:
                    if getattr(conn.laddr, 'port', None) == port:
                        logging.info(f"Killing process {proc.pid} ({proc.name()}) using port {port}...")
                        proc.kill()
                        logging.info("Process killed.")
                        return True
        logging.info(f"No process found using port {port}.")
        return False
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
        result = subprocess.run(['pkill', 'chrome'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            logging.info("All Chrome processes have been terminated.")
        elif "No matching processes" in result.stderr:
            logging.info("No Chrome processes found or an error occurred.")
        else:
            logging.info(f"Unknown error occurred: {result.stderr.strip()}")
    except Exception as e:
        logging.info(f"An error occurred: {e}")


def read_json_file(filepath):
    lock = FileLock(filepath + ".lock")
    while True:
        try:
            with lock.acquire(timeout=1):  # Try to acquire the lock with a short timeout
                with open(filepath, 'r') as file:
                    data = json.load(file)
                return data
        except TimeoutError:
            logging.info("Waiting for lock to be released...")
            time.sleep(1)  # Wait before trying again

# Initialize bot
async def echo(websocket, path):
    def get_file_modification_time(filepath):
        return os.path.getmtime(filepath)

    filepath = base_path
    last_mod_time = get_file_modification_time(filepath)
    connected.add(websocket)
    try:
        while True:
            try:
                # current_mod_time = get_file_modification_time(filepath)
                # if current_mod_time != last_mod_time:
                data = read_json_file(filepath)
                if data:
                    # logging.info("File has been updated.")
                        # last_mod_time = current_mod_time
                    await websocket.send(json.dumps({"data": data}))
                    await asyncio.sleep(1)  # Adjust the sleep duration as needed
            except FileNotFoundError:
                logging.info(f"File {filepath} not found.")
                break
            except Exception as e:
                logging.info(f"An error occurred: {e}")
                break
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
        for ws in set(connected):  # Create a shallow copy of the connected set
            try:
                await ws.ping()
            except Exception as e:
                logging.info(f"Ping error: {e}")
        await asyncio.sleep(10)  # Ping every 10 seconds (adjust as needed)

if __name__ == '__main__':
    connected = set()
    logging.info('WebSocket server starting...')

    start_server = websockets.serve(echo, "0.0.0.0", 8765)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    # loop.create_task(ping())
    loop.run_forever()

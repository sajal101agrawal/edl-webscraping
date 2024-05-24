from bot import *
import subprocess


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
        result = subprocess.run(['pkill', 'chrome'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print("All Chrome processes have been terminated.")
        elif "No matching processes" in result.stderr:
            print("No Chrome processes found or an error occurred.")
        else:
            print(f"Unknown error occurred: {result.stderr.strip()}")
    except Exception as e:
        print(f"An error occurred: {e}")

async def scrape():
    while True:
        try:
            bot_ = Bot()
            bot_.get_driver()
            bot_.work()
            await bot_.write_data_in_json()
        except:
            pass
        finally:
            kill_chrome_drivers()

scrape()

import subprocess
import asyncio
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
            await bot_.get_driver()  # Ensure get_driver is async if it needs to be
            await bot_.work()        # Ensure work is async if it needs to be
            await bot_.write_data_in_json()
        except Exception as e:
            print(f"An error occurred during scraping: {e}")
        finally:
            kill_chrome_drivers()
        await asyncio.sleep(10)  # Adjust the sleep interval as needed

# Run the scrape function using asyncio
if __name__ == "__main__":
    asyncio.run(scrape())

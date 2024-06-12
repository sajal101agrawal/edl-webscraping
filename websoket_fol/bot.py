import random, time, os, json, asyncio
from selenium_stealth import stealth
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.action_chains import ActionChains
import logging
from filelock import FileLock


logging.basicConfig(filename='api.log',level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

import random, time


def random_sleep(a=5, b=9):
    acc = random.randint(a, b)
    logging.info(f"random sleep : {acc}")
    time.sleep(acc)


chromedriver_path = os.path.join(os.getcwd(), "chromedriver")
chrome_binary_path = "/usr/bin/google-chrome"


class Bot:

    def return_driver(self):
        self.get_driver()
        return self.check_login()

    def get_local_driver(self):
        """Start webdriver and return state of it."""
        from selenium import webdriver

        for _ in range(30):
            options = webdriver.ChromeOptions()
            options.add_argument("--lang=en")  # Set webdriver language to English.
            options.add_argument("log-level=3")  # No logs is printed.
            options.add_argument("--mute-audio")  # Audio is muted.
            options.add_argument("--enable-webgl-draft-extensions")
            options.add_argument("--mute-audio")
            options.add_argument("--ignore-gpu-blocklist")
            options.add_argument("--disable-dev-shm-usage")
            # options.add_argument("--headless")
            prefs = {
                "credentials_enable_service": True,
                "profile.default_content_setting_values.automatic_downloads": 1,
                "download.prompt_for_download": False,  # Optional, suppress download prompt
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
                "profile.password_manager_enabled": True,
            }
            options.add_experimental_option("prefs", prefs)
            options.add_argument("--no-sandbox")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--enable-javascript")
            options.add_argument("--enable-popup-blocking")
            options.add_argument("--no-sandbox")  # Set webdriver language to English.
            options.add_argument("--disable-dev-shm-usage")
            try:
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
                driver.get("https://www.google.com")
                # breakpoint()
                # with open('cookies.pkl', 'rb') as file: cookies = pickle.load(file)
                # for cookie in cookies: driver.add_cookie(cookie)
                break
            except Exception as e:
                logging.info(e)

        self.driver = driver
        return self.driver

    def get_driver(self):
        """Start webdriver and return state of it."""
        for _ in range(30):
            """Start webdriver and return state of it."""
            from undetected_chromedriver import Chrome, ChromeOptions

            options = ChromeOptions()
            options.add_argument("--lang=en")  # Set webdriver language to English.
            options.add_argument("log-level=3")  # No logs is printed.
            options.add_argument("--mute-audio")  # Audio is muted.
            options.add_argument("--enable-webgl-draft-extensions")
            options.add_argument("--mute-audio")
            options.add_argument("--ignore-gpu-blocklist")
            options.add_argument("--disable-dev-shm-usage")
            # options.add_argument("--headless")
            prefs = {
                "credentials_enable_service": True,
                "profile.default_content_setting_values.automatic_downloads": 1,
                "download.prompt_for_download": False,  # Optional, suppress download prompt
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
                "profile.password_manager_enabled": True,
            }
            options.add_experimental_option("prefs", prefs)
            options.add_argument("--no-sandbox")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--enable-javascript")
            options.add_argument("--enable-popup-blocking")

            options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
            try:
                driver = Chrome(options=options, version_main=125)
                driver.get("https://www.google.com")
                self.driver = driver
                # self.driver.execute_cdp_cmd('Network.enable', {})

                # # Intercepting responses
                # self.driver.execute_cdp_cmd(
                #     'Network.setRequestInterception',
                #     {'patterns': [{'urlPattern': '*'}]}
                # )

                # self.driver.responses = []

                # def response_listener(request_id, url):
                #     def handle_response(response):
                #         if 'response' in response and 'requestId' in response and response['requestId'] == request_id:
                #             if '/data/update?' in url:
                #                 self.driver.responses.append({
                #                     'url': url,
                #                     'body': self.driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})['body']
                #                 })

                #     return handle_response

                # def request_will_be_sent(params):
                #     url = params['request']['url']
                #     if '/data/update?' in url:
                #         self.driver.request_ids[params['requestId']] = url

                # self.driver.request_ids = {}

                # def response_received(params):
                #     request_id = params['requestId']
                #     if request_id in self.driver.request_ids:
                #         url = self.driver.request_ids.pop(request_id)
                #         self.driver.execute_cdp_cmd(
                #             'Network.getResponseBody',
                #             {'requestId': request_id},
                #             response_listener(request_id, url)
                #         )

                # Adding listeners
                # self.driver.add_listener('Network.requestWillBeSent', request_will_be_sent)
                # self.driver.add_listener('Network.responseReceived', response_received)
                return self.driver
            except Exception as e:
                print(e)
                logging.info(e)

        return self.driver

    def find_element(
        self, element, locator, locator_type=By.XPATH, timeout=10, page=None, bulk=False
    ):
        """
        element      : name of element,
        locator      : xpath or other locator text,
        locator_type : locator type,
        timeout      : default 10,

        Find an element, return it, or return None;
        """
        try:
            if timeout > 0:
                wait_obj = WebDriverWait(self.driver, timeout)
                ele = (
                    wait_obj.until(
                        EC.presence_of_element_located((locator_type, locator))
                    )
                    if not bulk
                    else wait_obj.until(
                        EC.presence_of_all_elements_located((locator_type, locator))
                    )
                )
            else:
                logging.info(f"Timeout is less or equal zero: {timeout}")
                ele = (
                    self.driver.find_element(by=locator_type, value=locator)
                    if not bulk
                    else self.driver.find_elements(by=locator_type, value=locator)
                )
            if page:
                logging.info(f'Found the element "{element}" in the page "{page}"')
            else:
                logging.info(f"Found the element: {element}")
            return ele
        except Exception as e:
            if page:
                logging.info(f'Cannot find the element "{element}"' f' in the page "{page}"')
            else:
                logging.info(f"Cannot find the element: {element}")
                logging.info(e)

    def click_element(self, element, locator, locator_type=By.XPATH, timeout=10):
        """Find an element, then click and return it, or return None"""
        ele = self.find_element(element, locator, locator_type, timeout=timeout)

        if ele:
            self.ensure_click(ele)
            logging.info(f"Clicked the element: {element}")
            return ele

    def input_text(
        self,
        text,
        element,
        locator,
        locator_type=By.XPATH,
        timeout=10,
        hide_keyboard=True,
    ):
        """Find an element, then input text and return it, or return None"""

        ele = self.find_element(
            element, locator, locator_type=locator_type, timeout=timeout
        )

        if ele:
            for i in range(3):
                try:
                    ele.clear()
                    ele.send_keys(text)
                    logging.info(f'Inputed "{text}" for the element: {element}')
                    return ele
                except:
                    ...

    def ScrollDown(self, px):
        self.driver.execute_script(f"window.scrollTo(0, {px})")

    def ensure_click(self, element, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(element)
            )
            element.click()
        except :
            try:
                self.driver.execute_script("arguments[0].click();", element)
            except:
                actions = ActionChains(self.driver)
                actions.move_to_element(element).click().perform()


    def new_tab(self):
        self.driver.find_element(By.XPATH, "/html/body").send_keys(Keys.CONTROL + "t")

    def random_sleep(self, a=3, b=7):
        import time, os

        random_time = random.randint(a, b)
        logging.info(f"time sleep randomly : {random_time}")
        time.sleep(random_time)

    def getvalue_byscript(self, script="", reason=""):
        """made for return value from ele or return ele"""
        if reason:
            logging.info(f"Script execute for : {reason}")
        else:
            logging.info(f"execute_script : {script}")
        value = self.driver.execute_script(f"return {script}")
        return value

    def CloseDriver(self):
        try:
            self.driver.quit()
            logging.info("Driver is closed !")
        except Exception as e:
            ...

    def TestRunDriver(self, driver: webdriver):
        self.driver = driver
        try:
            self.driver.current_url
            return True
        except:
            return False

    def close_others_tab(self):
        for window in self.driver.window_handles[1:]:
            self.driver.switch_to.window(window)
            self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        ...

    def login(self):
        self.driver.get("https://div.edl.ch")
        if self.input_text("beag_barr", "username", "username", By.ID):
            self.input_text("P4r1s13nn3!86", "password", "password", By.ID)
            self.click_element("submitbutton", "submitbutton", By.ID)

    
    def work(self):
        numbers_tr_ele = []
        l_tr_table = []
        engines_links = []
        l_table = ""

        self.login()
        table = self.find_element("Table", "table", By.TAG_NAME)
        tbody = table.find_elements(By.TAG_NAME, "tbody")
        if not tbody: return False
        tbody = tbody[0]
        numbers_tr_ele = tbody.find_elements(By.TAG_NAME, "tr")

        for tr_tag in numbers_tr_ele:
            tr_a_tag = tr_tag.find_elements(
                By.XPATH, '//td[@data-menu_uuid="o.name"]/a'
            )
            if tr_a_tag:
                tr_a_tag[0].click()

                self.click_element("Link btn", '//*[@id="ui-id-5"]')
                l_table = self.find_element(
                    "object table",
                    "mst-table_layout-processed",
                    By.CLASS_NAME,
                    bulk=True,
                )
                # l_table = self.driver.find_elements(By.CLASS_NAME,'mst-table_layout-processed')
                if l_table:
                    l_tbody = l_table[0].find_elements(By.TAG_NAME, "tbody")

                    if l_tbody:
                        l_tr_table = l_tbody[0].find_elements(By.TAG_NAME, "tr")
                        if l_tr_table:
                            use_link = l_tr_table[0].find_elements(
                                By.XPATH, '//td[@data-menu_uuid="use"]/a'
                            )
                            if use_link:
                                engines_links.append(use_link[0].get_attribute("href"))

                self.driver.back()
                self.driver.refresh()

        self.track_window_list = []
        for use_link in engines_links:
            self.driver.get(use_link)
            iframe = ""
            iframe = self.find_element("iframe", "iframe", By.TAG_NAME)
            if iframe:
                main_window = self.driver.window_handles[0]
                logging.info(main_window)
                self.driver.switch_to.frame(iframe)
                all_btn_id = ['group_f0000006' ]
                # all_btn_id = ['group_f0000006','group_f0000005','group_f0000007', 'group_f0000008','group_f0000009',
                #             'group_f000000a', 'group_f000000b', 'group_f000000c', 'group_f000000d', ]
                previous_len = 1
                for id in all_btn_id:
                    self.click_element(f'{id} id',id, By.ID)
                    random_sleep(5,7)
                    for i in range(3):
                        if len(self.driver.window_handles) == previous_len:
                            self.click_element(f'{id} id',id, By.ID)
                            random_sleep(5,7)
                        if i == 2 and len(self.driver.window_handles) == previous_len:
                            raise RuntimeError("The number of driver's windows did not increase as expected.")
                    previous_len = len(self.driver.window_handles) 
                for i in self.driver.window_handles[1:]: self.track_window_list.append(i)
                # random_sleep()
                # self.click_element('info', 'group_f000000f', By.ID)
                # self.random_sleep(7)

                # for window in self.driver.window_handles:
                #     self.driver.switch_to.window(window)
                #     if 'WebGE/193i_011_Uebersicht_UV.html' in self.driver.current_url :
                #         break

                # self.click_element('info', 'group_f000000f', By.ID)
                # self.random_sleep(7)
                # for window in self.driver.window_handles[8:]:
                #     self.driver.switch_to.window(window)
                #     if 'WebGE/ZM111_01.html' in self.driver.current_url :
                #         self.track_window_list.append(window)
                #         self.diff_window = window
                #         break
                # logging.info(len(self.driver.window_handles))
                # # breakpoint()
                # logs = self.driver.get_log("performance") 
                # for i in self.process_browser_logs_for_network_events(logs):print(i)

                # # for entry in self.process_browser_logs_for_network_events(log_entries):respon.append(entry)
                # self.driver.switch_to.window(self.driver.window_handles[0])
                # # self.driver.switch_to.window(self.track_window_list[0])
                # self.driver.switch_to.default_content()
                # self.driver.switch_to.frame(
                #     self.find_element("iframe", "iframe", By.TAG_NAME)
                #     )


    def return_main_data(self):
        variabless = {
            "main kw": "useclip005f007a kW",
            "Strom L1..L3 AVG": "useclip005f0073 A",
            "Scheinleistung L1..L3": "useclip005f0081 kVA",
            "Blindleistung L1..L3": "useclip005f0088 kVAR",
            
            # "Leistung": {
            #     "Leistung L1": "useclip005f005e kW",
            #     "Leistung L2": "useclip005f0065 kW",
            #     "Leistung L3": "useclip005f006c kW",
            # },
            # "CosPhi/Frequenz/Harmonie": {
            #     "CosPhi L1": "useclip005f001f",
            #     "CosPhi L2": "useclip005f0026",
            #     "CosPhi L3": "useclip005f002d",
            # },
            # "Blindleistung/Energie": {
            #     "Blindleistung L1": "useclip005f0049 kVAR",
            #     "Blindleistung L2": "useclip005f0050 kVAR",
            #     "Blindleistung L3": "useclip005f0057 kVAR",
            # },
            # "Spannungen": {
            #     "Spannung L1-L2": "useclip005f0034 V",
            #     "Spannung L2-L3": "useclip005f003b V",
            #     "Spannung L3-L1": "useclip005f0042 V",
            # },
            # "Scheinleistung/Energie": {
            #     "Scheinleistung L1": "useclip005f000a kVA",
            #     "Scheinleistung L2": "useclip005f0011 kVA",
            #     "Scheinleistung L3": "useclip005f0018 kVA",
            # },
        }
        
        data = {}
        check_bool = False
        for key, value in variabless.items():
            if isinstance(value, dict):
                value_resp = self.scrap_data2(value)
                if value_resp != "":
                    data[key] = value_resp
                else:
                    check_bool = True
                    break
            else :
                value_resp = self.scrap_data1(value)
                if value_resp != "":
                    data[key] = value_resp
                else:
                    check_bool = True
                    break

        # if check_bool == True:
        #     data = {}
        #     variabless = {
        #         "Gesamtleistung L1..L3": "useclip0043007a kW",
        #         "Scheinleistung Strom L1": "useclip00430073 A",
        #         "Scheinleistung Strom L2": "useclip004300b1 A",
        #         "Scheinleistung Strom L3": "useclip004300aa A",
                
        #         "Leistung": {
        #             "Leistung L1": "useclip0043005e kW",
        #             "Leistung L2": "useclip00430065 kW",
        #             "Leistung L3": "useclip0043006c kW",
        #         },
        #         "CosPhi/Frequenz/Harmonie": {
        #             "CosPhi L1": "useclip0043001f",
        #             "CosPhi L2": "useclip00430026",
        #             "CosPhi L3": "useclip0043002d",
        #         },
        #         "Blindleistung/Energie": {
        #             "Blindleistung L1": "useclip00430049 kVAR",
        #             "Blindleistung L2": "useclip00430050 kVAR",
        #             "Blindleistung L3": "useclip00430057 kVAR",
        #         },
        #         "Spannungen": {
        #             "Spannung L1-L2": "useclip00430034 V",
        #             "Spannung L2-L3": "useclip0043003b V",
        #             "Spannung L3-L1": "useclip00430042 V",
        #         },
        #         "Scheinleistung/Energie": {
        #             "Scheinleistung L1": "useclip0043000a kVA",
        #             "Scheinleistung L2": "useclip00430011 kVA",
        #             "Scheinleistung L3": "useclip00430018 kVA",
        #         },
        #     }
            
        #     data = {}
        #     for key, value in variabless.items():
        #         if isinstance(value, dict):
        #             data[key] = self.scrap_data21(value)
        #         else :
        #             data[key] = self.scrap_data1(value)
        return data
    
    def process_browser_logs_for_network_events(self,logs):
        """
        Return only logs which have a method that start with "Network.response", "Network.request", or "Network.webSocket"
        since we're interested in the network events specifically.
        """
        for entry in logs:
            log = json.loads(entry["message"])["message"]
            if (
                    "Network.response" in log["method"]
            ):
                yield log


    async def return_main_data_for_all_windows_parallel_helper(self, win):
        self.driver.switch_to.window(win)
        # self.driver.get_log()
        # if self.driver.current_window_handle == self.diff_window:
        #     Energie_Tarif_1 = self.find_element('useclip00760040 id', 'useclip00760040', By.ID)
        #     Wirkleistung_Total = self.find_element('useclip00760039 id', 'useclip00760039', By.ID)
        #     return {
        #         'Energie Tarif 1': f'{Energie_Tarif_1.text.strip()} W',
        #         'Wirkleistung Total': f'{Wirkleistung_Total.text.strip()} kWh'
        #     }
        return self.return_main_data()

    async def return_main_data_for_all_windows_parallel(self):
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            tasks = [loop.run_in_executor(executor, self.return_main_data_for_all_windows_parallel_helper, win) for win in self.track_window_list]
            results = await asyncio.gather(*tasks)
        return results

    
    def write_json_file(self, filepath, data):
        lock = FileLock(filepath + ".lock")
        try:
            with lock.acquire(timeout=10):  # Try to acquire the lock with a short timeout
                with open(filepath, 'w') as file:
                    json.dump(data, file, indent=4)
                return
        except TimeoutError:
            logging.info("Waiting for lock to be released...")
            time.sleep(1)  # Wait before trying again

    
    async def write_data_in_json(self):
        self.driver.switch_to.window(self.track_window_list[0])
        while True:
            filepath = 'data.json'
            # main_data = await self.return_main_data_for_all_windows_parallel()
            main_data = self.return_main_data()
            if main_data:
                self.write_json_file(filepath, main_data)
                time.sleep(0.3)
                
    def scrap_data1(self,  value : str):
        rt_v = ''
        parts = value.split(' ')
        kw = parts[1] if len(parts) > 1 else ''
        idd = parts[0]
        ele = self.driver.find_elements(By.ID,idd)
        if ele :
            rt_v = ele[0].text 
            if kw :
                rt_v += ' ' + kw
            return rt_v
        return ''
        
    def scrap_data2(self, dictt : dict):
        tmp = {}
        for key, value in dictt.items():
            if self.scrap_data1(value) != "":
                tmp[key] = self.scrap_data1(value)
            else:
                return ''
        
        return tmp

    def scrap_data21(self, dictt : dict):
        tmp = {}
        for key, value in dictt.items():
            tmp[key] = self.scrap_data1(value)
        return tmp
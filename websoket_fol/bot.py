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

import random, time


def random_sleep(a=5, b=9):
    acc = random.randint(a, b)
    print("random sleep :", acc)
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
            options.add_argument("--headless")
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
                print(e)

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
            try:
                breakpoint()
                driver = Chrome(options=options, version_main=121)
                driver.get("https://www.google.com")
                break
            except Exception as e:
                print(e)

        self.driver = driver
        return self.driver

    def find_element(
        self,
        element,
        locator,
        locator_type=By.XPATH,
        page=None,
        timeout=10,
        condition_func=EC.presence_of_element_located,
        condition_other_args=tuple(),
    ):
        """Find an element, then return it or None.
        If timeout is less than or requal zero, then just find.
        If it is more than zero, then wait for the element present.
        """
        try:
            if timeout > 0:
                wait_obj = WebDriverWait(self.driver, timeout)
                ele = wait_obj.until(
                    EC.presence_of_element_located((locator_type, locator))
                )
                # ele = wait_obj.until( condition_func((locator_type, locator),*condition_other_args))
            else:
                print(f"Timeout is less or equal zero: {timeout}")
                ele = self.driver.find_element(by=locator_type, value=locator)
            if page:
                print(f'Found the element "{element}" in the page "{page}"')
            else:
                print(f"Found the element: {element}")
            return ele
        except Exception as e:
            if page:
                print(f'Cannot find the element "{element}"' f' in the page "{page}"')
            else:
                print(f"Cannot find the element: {element}")

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
                print(f"Timeout is less or equal zero: {timeout}")
                ele = (
                    self.driver.find_element(by=locator_type, value=locator)
                    if not bulk
                    else self.driver.find_elements(by=locator_type, value=locator)
                )
            if page:
                print(f'Found the element "{element}" in the page "{page}"')
            else:
                print(f"Found the element: {element}")
            return ele
        except Exception as e:
            if page:
                print(f'Cannot find the element "{element}"' f' in the page "{page}"')
            else:
                print(f"Cannot find the element: {element}")
                print(e)

    def click_element(self, element, locator, locator_type=By.XPATH, timeout=10):
        """Find an element, then click and return it, or return None"""
        ele = self.find_element(element, locator, locator_type, timeout=timeout)

        if ele:
            self.driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", ele)
            self.ensure_click(ele)
            print(f"Clicked the element: {element}")
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
                    print(f'Inputed "{text}" for the element: {element}')
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
        except:
            self.driver.execute_script("arguments[0].click();", element)

    def new_tab(self):
        self.driver.find_element(By.XPATH, "/html/body").send_keys(Keys.CONTROL + "t")

    def random_sleep(self, a=3, b=7):
        import time, os

        random_time = random.randint(a, b)
        print("time sleep randomly :", random_time)
        time.sleep(random_time)

    def getvalue_byscript(self, script="", reason=""):
        """made for return value from ele or return ele"""
        if reason:
            print(f"Script execute for : {reason}")
        else:
            print(f"execute_script : {script}")
        value = self.driver.execute_script(f"return {script}")
        return value

    def CloseDriver(self):
        try:
            self.driver.quit()
            print("Driver is closed !")
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
        if tbody:
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

        for use_link in engines_links:
            self.driver.get(use_link)
            iframe = ""
            iframe = self.find_element("iframe", "iframe", By.TAG_NAME)
            if iframe:
                try:
                    self.driver.switch_to.frame(iframe)
                    random_sleep()
                    all_btn_id = ['group_f0000005','group_f0000007', 'group_f0000008','group_f0000009', 'group_f000000a', 'group_f000000b', 'group_f000000c', 'group_f000000d']
                    for id in all_btn_id:
                        self.driver.find_element(By.ID,id).click()
                        random_sleep(1,2)
                except:
                        ...
                finally:
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    self.driver.switch_to.default_content()
                    self.driver.switch_to.frame(
                        self.find_element("iframe", "iframe", By.TAG_NAME)
                        )

    def return_main_data(self):
        variabless = {
            "main kw": "useclip005f007a kW",
            "Strom L1..L3 AVG": "useclip005f0073 A",
            "Scheinleistung L1..L3": "useclip005f0081 kVA",
            "Blindleistung L1..L3": "useclip005f0088 kVAR",
            
            "Leistung": {
                "Leistung L1": "useclip005f005e kW",
                "Leistung L2": "useclip005f0065 kW",
                "Leistung L3": "useclip005f006c kW",
            },
            "CosPhi/Frequenz/Harmonie": {
                "CosPhi L1": "useclip005f001f",
                "CosPhi L2": "useclip005f0026",
                "CosPhi L3": "useclip005f002d",
            },
            "Blindleistung/Energie": {
                "Blindleistung L1": "useclip005f0049 kVAR",
                "Blindleistung L2": "useclip005f0050 kVAR",
                "Blindleistung L3": "useclip005f0057 kVAR",
            },
            "Spannungen": {
                "Spannung L1-L2": "useclip005f0034 V",
                "Spannung L2-L3": "useclip005f003b V",
                "Spannung L3-L1": "useclip005f0042 V",
            },
            "Scheinleistung/Energie": {
                "Scheinleistung L1": "useclip005f000a kVA",
                "Scheinleistung L2": "useclip005f0011 kVA",
                "Scheinleistung L3": "useclip005f0018 kVA",
            },
        }
        
        data = {}
        for key, value in variabless.items():
            try:
                if isinstance(value, dict):
                    data[key] = self.scrap_data1(value)
                else :
                    data[key] = self.scrap_data2(value)
            except:pass
        return data

    async def return_main_data_for_all_windows_parallel_helper(self, win):
        self.driver.switch_to.window(win)
        return self.return_main_data()

    async def return_main_data_for_all_windows_parallel(self):
        with ThreadPoolExecutor() as executor:
            tasks = [self.return_main_data_for_all_windows_parallel_helper(win) for win in self.driver.window_handles[1:]]
            results = await asyncio.gather(*tasks)
        return results
                
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
            tmp[key] = self.scrap_data1(value)
        
        return tmp

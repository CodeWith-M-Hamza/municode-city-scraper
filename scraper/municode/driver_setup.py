from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

def get_driver(headless: bool = False) -> webdriver.Chrome:
    options=Options()
    if headless:
        options.add_argument('--headless=new')
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver=webdriver.Chrome(options=options)
    driver.implicitly_wait(0)
    return driver 
    
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def close_tour_popup(driver, xpaths, logger, timeout=5):
    close_btns = driver.find_elements(By.XPATH, xpaths["hopsotch_bubble_container"])

    if not close_btns:
        logger.error(f"Popup close button not found | url={driver.current_url} | xpath={xpaths['hopsotch_bubble_container']}")
        return

    try:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpaths["hopsotch_bubble_container"]))
        )
        close_btns[0].click()
    except Exception as e:
        logger.error(f"Popup click failed | url={driver.current_url} | error={e}")
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def extract_table(driver, table_wrapper_el, xpaths, logger):
    """
    Expands table, extracts headers+rows, closes table, returns data.
    """
    table_data = {"headers": [], "rows": []}

    # Step 1: Expand button (required)
    expand_btns = table_wrapper_el.find_elements(By.XPATH, xpaths["table_expand_button_relative"])
    if not expand_btns:
        logger.error(
            f"Expand button not found | url={driver.current_url} | xpath={xpaths['table_expand_button_relative']}"
        )
        return table_data

    try:
        expand_btns[0].click()
    except Exception as e:
        logger.error(f"Expand button click failed | url={driver.current_url} | error={e}")
        return table_data

    # Step 2: Wait for expanded modal table (genuine wait, not a simple find)
    try:
        modal_table = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpaths["expanded_table"]))
        )
    except Exception as e:
        logger.error(
            f"Expanded table did not appear | url={driver.current_url} | xpath={xpaths['expanded_table']} | error={e}"
        )
        return table_data

    # Step 3: Extract headers (required)
    headers = modal_table.find_elements(By.XPATH, xpaths["table_headers_relative"])
    if not headers:
        logger.error(
            f"Table headers not found | url={driver.current_url} | xpath={xpaths['table_headers_relative']}"
        )
    table_data["headers"] = [h.text.strip() for h in headers]

    # Step 4: Extract rows (required)
    rows = modal_table.find_elements(By.XPATH, xpaths["table_rows_relative"])
    if not rows:
        logger.error(
            f"Table rows not found | url={driver.current_url} | xpath={xpaths['table_rows_relative']}"
        )
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        table_data["rows"].append([c.text.strip() for c in cells])

    # Step 5: Close button (required)
    close_btns = driver.find_elements(By.XPATH, xpaths["table_close_button"])
    if not close_btns:
        logger.error(
            f"Close button not found | url={driver.current_url} | xpath={xpaths['table_close_button']}"
        )
        return table_data

    try:
        close_btns[0].click()
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, xpaths["expanded_table"]))
        )
    except Exception as e:
        logger.error(f"Table close failed | url={driver.current_url} | error={e}")

    return table_data
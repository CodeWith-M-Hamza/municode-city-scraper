from scraper.municode.driver_setup import get_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper.municode.page_actions import close_tour_popup
from scraper.municode.chapter_scraper import get_chapters
from scraper.municode.section_scraper import get_sections
from scraper.logging_setup import get_logger
from selenium.webdriver.common.by import By
import json
import time


def load_xpaths(path="scraper/municode/xpaths/municode_xpaths.json"):
    with open(path, "r") as f:
        return json.load(f)


def run(start_url):
    xpaths = load_xpaths()
    logger = get_logger("municode")
    driver = get_driver(headless=False)
    all_data = []

    try:
        driver.get(start_url)
        time.sleep(4)

        # Wait for the sidebar to actually load before checking popup/chapters
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, xpaths["chapter_links3"]))
            )
        except Exception as e:
            logger.error(f"Page did not load in time | url={start_url} | error={e}")
            

        close_tour_popup(driver, xpaths, logger)

        chapters = get_chapters(driver, xpaths, logger)
        logger.info(f"Found {len(chapters)} chapters")

        for chapter in chapters:
            driver.get(chapter["url"])
            time.sleep(4)

            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located((By.XPATH, xpaths["section_chunk_wrapper"]))
                )
            except Exception as e:
                logger.error(
                    f"Sections did not load in time | chapter={chapter['title']} | url={chapter['url']} | error={e}"
                )
                continue

            sections = get_sections(driver, xpaths, logger)

            all_data.append({
                "chapter_title": chapter["title"],
                "chapter_url": chapter["url"],
                "sections": sections,
            })

    finally:
        driver.quit()

    return all_data


if __name__ == "__main__":
    result = run("https://library.municode.com/sd/salem/codes/code_of_ordinances?nodeId=CD_ORD_APXAZO")
    print(f"Scraped {len(result)} chapters")
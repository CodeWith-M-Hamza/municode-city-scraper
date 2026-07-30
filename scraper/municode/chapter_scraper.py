from selenium.webdriver.common.by import By


def get_chapters(driver, xpaths, logger):
    chapters = []

    link_elements = driver.find_elements(By.XPATH, xpaths["chapter_links3"])
    if not link_elements:
        logger.error(f"No chapter links found | url={driver.current_url} | xpath={xpaths['chapter_links3']}")

    title_elements = driver.find_elements(By.XPATH, xpaths["chapter_titles3"])
    if not title_elements:
        logger.error(f"No chapter titles found | url={driver.current_url} | xpath={xpaths['chapter_titles3']}")

    if len(link_elements) != len(title_elements):
        logger.error(
            f"Mismatch: {len(link_elements)} links vs {len(title_elements)} titles | url={driver.current_url}"
        )

    for link_el, title_el in zip(link_elements, title_elements):
        a_tags = link_el.find_elements(By.XPATH, xpaths["chapter_link_a_tag"])
        if not a_tags:
            logger.error(f"Chapter <a> tag not found | url={driver.current_url} | xpath={xpaths['chapter_link_a_tag']}")
            continue

        url = a_tags[0].get_attribute("href")
        title = title_el.text.strip()

        if not title:
            logger.error(f"Chapter title is empty | url={url}")

        chapters.append({"title": title, "url": url})

    return chapters
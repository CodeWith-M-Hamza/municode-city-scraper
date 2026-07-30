from selenium.webdriver.common.by import By
from scraper.municode.table_scraper import extract_table


def get_sections(driver, xpaths, logger):
    """
    Extracts all sections (title, body/table, cross-refs, history note)
    from the currently loaded chapter page.
    """
    sections = []

    chunk_elements = driver.find_elements(By.XPATH, xpaths["section_chunk_wrapper"])
    if not chunk_elements:
        logger.error(
            f"No section chunks found | url={driver.current_url} | xpath={xpaths['section_chunk_wrapper']}"
        )

    for chunk_el in chunk_elements:
        section_data = {
            "title": None,
            "has_table": False,
            "body_text": None,
            "table_data": None,
            "cross_references": [],
            "history_note": None,
        }

        # Title (required)
        title_els = chunk_el.find_elements(By.XPATH, xpaths["chunk_title_relative"])
        if title_els:
            section_data["title"] = title_els[0].text.strip()
            if not section_data["title"]:
                logger.error(f"Title found but empty | url={driver.current_url}")
        else:
            logger.error(
                f"Title xpath not found | url={driver.current_url} | xpath={xpaths['chunk_title_relative']}"
            )

        # Content wrapper (required)
        content_els = chunk_el.find_elements(By.XPATH, xpaths["chunk_content_relative"])
        if not content_els:
            logger.error(
                f"Content xpath not found | title={section_data['title']} | xpath={xpaths['chunk_content_relative']}"
            )
            sections.append(section_data)
            continue

        content_el = content_els[0]

        # Table vs plain text (table is optional, no error if absent)
        table_wrappers = content_el.find_elements(By.XPATH, xpaths["table_wrapper_relative"])
        if table_wrappers:
            section_data["has_table"] = True
            section_data["table_data"] = extract_table(driver, table_wrappers[0], xpaths, logger)
        else:
            section_data["body_text"] = content_el.text.strip()

        # Cross-references (optional, no error if absent)
        ref_elements = content_el.find_elements(By.XPATH, xpaths["cross_reference_relative"])
        section_data["cross_references"] = [r.text.strip() for r in ref_elements]

        # History note (optional, no error if absent)
        history_els = content_el.find_elements(By.XPATH, xpaths["history_note_relative"])
        if history_els:
            section_data["history_note"] = history_els[0].text.strip()

        sections.append(section_data)

    return sections
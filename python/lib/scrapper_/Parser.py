from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import re
from ..Errors import ParseError


class Parser:

    # --- CATEGORIE ---
    @classmethod
    def get_cate_name(cls, driver):
        try:
            driver.find_element(By.TAG_NAME, "h3")
            name = driver.text
            return name.split("•")[0]
        except NoSuchElementException:
            raise ParseError

    # --- WORK ---
    @classmethod
    def __get_name_and_year(cls, driver):
        try:
            name_and_year_el = driver.find_element(
                    By.CSS_SELECTOR,
                    ".h3.text-uppercase.text-break.fw-bold.mb-0")
            return name_and_year_el.text
        except NoSuchElementException:
            raise ParseError

    @classmethod
    def get_work_name(cls, driver) -> str:
        try:
            name_and_year_el = cls.__get_name_and_year(driver)
            return name_and_year_el.split("(")[0]
        except (NoSuchElementException, ParseError):
            raise ParseError

    @classmethod
    def get_work_year(cls, driver) -> str:
        try:
            name_and_year_el = cls.__get_name_and_year(driver)
            match = re.search(r"\((\d{4})\)", name_and_year_el)
            if match:
                return match.group(1)
            return ""
        except (NoSuchElementException, ParseError):
            raise ParseError

    @classmethod
    def get_work_price(cls, driver) -> str:
        try:
            price_container = driver.find_element(
                    By.CSS_SELECTOR, "#artwork_original_price")
            price_el = price_container.find_element(
                By.TAG_NAME, "span")
            return price_el.get_attribute("data-analytics-price")
        except NoSuchElementException:
            raise ParseError

    @classmethod
    def get_work_description(cls, driver) -> str:
        try:
            description_el = driver.find_element(
                    By.CSS_SELECTOR, "#full_description_text")
            description = driver.execute_script("""
                let el = arguments[0];

                let text = "";
                el.childNodes.forEach(node => {
                    if (node.nodeType === Node.TEXT_NODE) {
                        text += node.textContent;
                    }
                });

                return text.trim();
            """, description_el)
            return description
        except NoSuchElementException:
            raise ParseError

    @classmethod
    def get_work_size(cls, driver) -> str:
        try:
            size_el = driver.find_element(
                    By.CSS_SELECTOR,
                    "div.row ul.list-unstyled li.mt-2"
                    )
            # 🔹 Format 1 : 100 x 200 cm (avec virgules ou points)
            size = re.search(r"\d+(?:[.,]\d+)?\s*x\s*\d+(?:[.,]\d+)?\s*cm",
                             size_el.text)
            if size:
                return size.group()

            # 🔹 Format 2 : Hauteur 72cm, Largeur 54cm
            size_alt = re.search(
                r"Hauteur\s*(\d+(?:[.,]\d+)?)\s*cm,\s*Largeur\s*(\d+(?:[.,]\d+)?)\s*cm",
                size_el.text,
                re.IGNORECASE
            )
            if size_alt:
                height = size_alt.group(1)
                width = size_alt.group(2)
                return f"{height} x {width} cm"
            print(f"size: ({size_el.text})")
            raise ParseError
        except NoSuchElementException:
            raise ParseError

    @classmethod
    def get_work_img_url(cls, driver) -> str:
        try:
            img_container = driver.find_element(By.ID, "carousel_image")
            img_el = img_container.find_element(By.TAG_NAME, "img")
            img_url = img_el.get_attribute("src")
            return img_url
        except NoSuchElementException:
            raise ParseError

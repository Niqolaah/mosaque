from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from time import sleep
from .ParsedData import ParsedData
from .Parser import Parser
from.Errors import ParseError, CloudflairError

from typing import Any
import time
import random


class Scrapper:
    def __init__(self):
        self.__works = ParsedData()

    def scrap(self):
        url = "https://www.artmajeur.com/agnes-couret"
        try:
            self.scrap_works_categories(url)
            self.scrap_works(url)
            self.__works.print_work_list()
        except CloudflairError as e:
            raise CloudflairError(e)

    def scrap_works(self, url: str) -> None:
        url_list = self.__works.get_links_list()
        for i, url in enumerate(url_list):
            try:
                driver = self.__get_site(url)
            except CloudflairError:
                raise CloudflairError(f"Cloudflair error at {url}")

            try:
                name = Parser.get_work_name(driver)
            except ParseError:
                name = ""
            try:
                price = Parser.get_work_price(driver)
            except ParseError:
                price = ""
            try:
                description = Parser.get_work_description(driver)
            except ParseError:
                description = ""
            try:
                size = Parser.get_work_size(driver)
            except ParseError:
                size = ""
            try:
                year = Parser.get_work_year(driver)
            except ParseError:
                year = ""

            
            self.__works.update_work_by_url(
                url=url, name=name, year=year, size=size, price=price,
                description=description
            )
            driver.quit()
            print(f"Scrapped: {i+1}/{len(url_list)}")
            sleep(1)

    def scrap_works_categories(self, url: str) -> None:
        try:
            driver = self.__get_site(url, visibility=True)
        except CloudflairError:
            raise CloudflairError("Cloudflair Error at categories collecting")

        categories_container = driver.find_element(By.CSS_SELECTOR,
                                                   "#carousel_container")
        categories_elm = categories_container.find_elements(By.CSS_SELECTOR, ".py-4")
        print(f"{len(categories_elm)} categories found")

        for categorie in categories_elm:
            cate_name = Parser.get_cate_name(categorie)
            self.__works.add_categorie(cate_name, "")
            works_container_el = categorie.find_element(
                By.CSS_SELECTOR, ".swiper-wrapper.d-flex")
            works_el = works_container_el.find_elements(By.XPATH, "./*")
            for work_el in works_el:
                # work_name = work_el.find_element(By.CSS_SELECTOR,
                #                                  ".text-truncate.me-3")
                work_link = work_el.find_element(By.TAG_NAME, "a")
                self.__works.add_work(cate_name,
                                      work_link.get_attribute("href"))

        # self.__works.print_work_list()
        driver.quit()
        sleep(2)

    def __get_site(self, url: str, visibility: bool = True, retries: int = 5) -> Any:
        for attempt in range(retries):
            time.sleep(random.uniform(3, 7))
            options = uc.ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--window-position=-2000,0")
            options.add_argument("--window-size=1920,1080")


            driver = uc.Chrome(options=options, version_main=144)
            driver.get(url)
            driver.minimize_window()
            sleep(2)
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.ID, "YqYak7"))
                )
                print("Cloudflair protection detected, program will retry in 10 seconds")
                sleep(10)
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.ID, "YqYak7"))
                )
                driver.quit()
                sleep(30)
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.ID, "YqYak7"))
                )
                driver.quit()
                print(f"* Cloudflair bypass attempt failed: {attempt + 1}/{retries}*")

            except (NoSuchElementException, TimeoutException):
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)
                return driver
        raise CloudflairError

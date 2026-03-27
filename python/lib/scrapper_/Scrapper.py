import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep
from ..ParsedData import ParsedData
from .Parser import Parser
from ..Errors import ParseError, CloudflairError
from ..LogRecorder import LogRecorder, LogType

from typing import Any
import time
import os
import random


class Scrapper:
    def __init__(self, logrecorder: LogRecorder, works: ParsedData):
        self.__works= works
        self.__logs = logrecorder

    def scrap(self, visibility: bool = True):
        url = "https://www.artmajeur.com/agnes-couret"
        try:
            now = time.time()
            self.scrap_works_categories(url, visibility)
            self.scrap_works_links(visibility)
            self.scrap_works(url, visibility)
            self.__logs.add_log(f"Scrapping finised in {time.time() - now}s",
                                LogType.LOGSUCCESS)
            self.download_all_imgs(visibility=True)
            self.__works.print_work_list()
        except CloudflairError as e:
            raise CloudflairError(e)
        finally:
            self.__works.write_works()

    def test_scrap_images(self, save_url: str) -> None:
        self.__works.init_last_registry(save_url)
        self.__works.print_work_list()
        self.download_all_imgs(visibility=False)

    def scrap_works(self, url: str, visibility: bool) -> None:
        url_list = self.__works.get_links_list()
        for i, url in enumerate(url_list):
            try:
                driver = self.__get_site(url, visibility=visibility, work_page=True)
            except CloudflairError:
                error_str = f"Cloudflair error at work: {url}"
                self.__logs.add_log(error_str, LogType.LOGERROR)
                raise CloudflairError(error_str)

            status = False

            try:
                name = Parser.get_work_name(driver)
            except ParseError:
                self.__logs.add_log(f"Name not found at {url}",
                                    LogType.LOGINFO)
                print("Name is null")
                name = ""
            try:
                price = Parser.get_work_price(driver)
            except ParseError:
                # self.__logs.add_log(f"Price not found at {url}",
                #                     LogType.LOGINFO)
                price = "0"
                status = True
            try:
                description = Parser.get_work_description(driver)
            except ParseError:
                self.__logs.add_log(f"Description not found at {url}",
                                    LogType.LOGINFO)
                description = ""
            try:
                size = Parser.get_work_size(driver)
            except ParseError:
                self.__logs.add_log(f"Size not found at {url}",
                                    LogType.LOGINFO)
                print("Size is null")
                size = ""
            try:
                year = Parser.get_work_year(driver)
            except ParseError:
                self.__logs.add_log(f"Year not found at {url}",
                                    LogType.LOGINFO)
                year = ""
            try:
                img_url = Parser.get_work_img_url(driver)
            except ParseError:
                self.__logs.add_log(f"Image not found at {url}",
                                    LogType.LOGINFO)
                img_url = None

            img_file_name = url.split("/")[-1] + ".png"
            
            self.__works.update_work_by_url(
                url=url, name=name, year=year, size=size, price=price,
                description=description, status=status, img_url=img_url,
                img_file_name=img_file_name
            )
            self.__logs.add_log((f"Work ({name}) successfully scrapped "
                                f"({i+1}/{len(url_list)})"),
                                LogType.LOGSUCCESS)
            driver.quit()
            sleep(1)

    def scrap_works_links(self, visibility: bool) -> None:
        for cate_dict in self.__works.get_cate_as_list():
            try:
                driver = self.__get_site(cate_dict["link"], visibility=visibility)
            except CloudflairError:
                error_str = "Cloudflair Error at work link collecting"
                self.__logs.add_log(error_str, LogType.LOGERROR)
                raise CloudflairError(error_str)
            
            try:
                works = Parser.get_works_el(driver)
            except ParseError:
                error_str = "Works not found"
                self.__logs.add_log(error_str, LogType.LOGERROR)
                raise ParseError(error_str)
            
            for work in works:
                try:
                    name = Parser.get_work_name_by_cate(work)
                    link = Parser.get_work_link_by_cate(work)

                    print(f"name: {name}, link: {link}")
                except ParseError:
                    error_str = "Works not found"
                    self.__logs.add_log(error_str, LogType.LOGERROR)
                    raise ParseError(error_str)
                self.__works.add_work(categorie=cate_dict["name"],
                                      link=link,
                                      name=name)
            driver.quit()

    def scrap_works_categories(self, url: str, visibility: bool) -> None:
        try:
            driver = self.__get_site(url, visibility=visibility)
        except CloudflairError:
            error_str = "Cloudflair Error at categories collecting"
            self.__logs.add_log(error_str, LogType.LOGERROR)
            raise CloudflairError(error_str)

        categories_container = driver.find_element(By.CSS_SELECTOR,
                                                   "#carousel_container")
        categories_elm = categories_container.find_elements(By.CSS_SELECTOR,
                                                            ".py-4")
        self.__logs.add_log(("Successfully found"
                            f" {len(categories_elm)} categories"),
                            LogType.LOGSUCCESS)

        for categorie in categories_elm:
            try:
                cate_name = Parser.get_cate_name(categorie)
                cate_link = Parser.get_cate_link(categorie)
            except ParseError:
                self.__logs.add_log("Categorie name not found",
                                    LogType.LOGINFO)
                cate_name = "NameError"

            self.__works.add_categorie(cate_name, cate_link)
            # works_container_el = categorie.find_element(
            #     By.CSS_SELECTOR, ".swiper-wrapper.d-flex")
            # works_el = works_container_el.find_elements(By.XPATH, "./*")
            # for work_el in works_el:
            #     work_link = work_el.find_element(By.TAG_NAME, "a")
            #     self.__works.add_work(categorie=cate_name,
            #                           link=work_link.get_attribute("href"))

        driver.quit()
        sleep(2)

    def download_all_imgs(self, visibility: bool):
        for img in self.__works.get_imgs_list():
            try:
                self.download_work_img(img, visibility)
            except Exception as e:
                self.__logs.add_log((f"Cannot download {img['file_name']}"
                                     f" at {img['link']}: {e}"),
                                    LogType.LOGINFO)

    def download_work_img(self, img_dict: dict[str, str],
                          visibility: bool) -> None:
        os.makedirs("imgs", exist_ok=True)

        url = img_dict["link"]
        img_name = img_dict["file_name"]
        filename = os.path.join("imgs", img_name)

        try:
            driver = self.__get_site(url, visibility=visibility)
            img = driver.find_element(By.TAG_NAME, "img")
            with open(filename, "wb") as f:
                f.write(img.screenshot_as_png)

            self.__logs.add_log("Image successfully downloaded",
                                LogType.LOGSUCCESS)
        except CloudflairError:
            error_str = f"Cloudflair: Impossible to download {url}"
            self.__logs.add_log(error_str, LogType.LOGERROR)
            os.remove(filename)
            raise CloudflairError(error_str)
        except TimeoutException:
            error_str = f"Timeout: Impossible to download {url}"
            self.__logs.add_log(error_str, LogType.LOGERROR)
            os.remove(filename)
            raise TimeoutException(error_str)
        finally:
            driver.quit()

    def __get_site(self, url: str, visibility: bool, retries: int = 5, work_page:bool = False) -> Any:
        for attempt in range(retries):
            time.sleep(random.uniform(3, 7))
            options = uc.ChromeOptions()
            options.add_argument(
                "--disable-blink-features=AutomationControlled")
            if not visibility:
                options.add_argument("--window-position=-2000,0")
                options.add_argument("--window-size=1920,1080")

            driver = uc.Chrome(options=options, version_main=144)
            driver.set_page_load_timeout(30)
            if not visibility:
                driver.minimize_window()

            driver.get(url)
            sleep(2)
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.ID, "YqYak7"))
                )
                print("Cloudflair protection detected, "
                      "program will retry in 10 seconds")
                sleep(10)
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.ID, "YqYak7"))
                )
                print("Cloudflair protection detected, "
                      "program will retry in 30 seconds")
                sleep(30)
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.ID, "YqYak7"))
                )
                driver.quit()
                error_str = (f"* Cloudflair bypass attempt failed: "
                             f"{attempt + 1}/{retries}*")
                self.__logs.add_log(error_str, LogType.LOGINFO)

            except (NoSuchElementException, TimeoutException):
                time.sleep(1)
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)
                if(work_page):
                    time.sleep(1)
                    try:
                        body = driver.find_element(By.ID,
                                            "my-page")
                        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                        driver.execute_script("document.body.click();")
                        sleep(1)
                    except Exception as e:
                        pass
                return driver
        raise CloudflairError

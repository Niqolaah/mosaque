from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from time import time
from .ParsedData import ParsedData



from typing import Any

class Scrapper:
    def __init__(self):
        self.__works = ParsedData()
    

    def scrap_site(self, url: str) -> None:

        driver = self.__get_site(url)

        categories_container = driver.find_element(By.CSS_SELECTOR, "#carousel_container")
        categories_elm = categories_container.find_elements(By.CSS_SELECTOR, ".py-4")
        print(f"Nombre trouve: {len(categories_elm)}")

        for categorie in categories_elm:
            title = categorie.find_element(By.TAG_NAME, "h3")
            cate_name = title.text
            self.__works.add_categorie(cate_name, "")
            works_container_el = categorie.find_element(By.CSS_SELECTOR, ".swiper-wrapper.d-flex")
            works_el = works_container_el.find_elements(By.XPATH, "./*")
            for work_el in works_el:
                work_name = work_el.find_element(By.CSS_SELECTOR, ".text-truncate.me-3")
                work_link = work_el.find_element(By.TAG_NAME, "a")
                self.__works.add_work(cate_name, work_name.text, work_link.get_attribute("href"))

        self.__works.print_work_list()

        while(True):
            pass
        driver.quit()


    def __get_site(self, url: str) -> Any:
        options = Options()
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        time_record = time()
        while(time() - time_record < 5):
            pass
        try:
            cloudflare_btn = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, "cb-lb"))
            )
            print("*Cloudflair protection detected*")
            cloudflare_btn.click()
        except (NoSuchElementException, TimeoutException) : 
            print("*No cloudflair protection detected*")

        return driver

                
    
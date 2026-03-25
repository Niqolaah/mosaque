from typing import Union
from datetime import datetime
import os


class ParsedData:

    def __init__(self):
        self.__works: dict[str, dict[str, Union[str, list[Work]]]] = {}

    # dict  {
    #       "categorie": {
    #                    link": "url"
    #                    list": [Works]
    #                    }
    #       }
    def add_work(self, categorie, link, name="None", year=0,
                 size="None", status="None") -> None:
        if categorie in self.__works:
            self.__works[categorie]["list"].append(
                Work(link=link, name=name, year=year, size=size, status=status)
            )

    def add_categorie(self, name, link) -> None:
        if name not in self.__works:
            self.__works[name] = {"link": link, "list": []}

    def print_work_list(self) -> None:
        for categorie, content in self.__works.items():
            print("========================")
            print(f"- {categorie} ({content['link']}): ")
            for work in content["list"]:
                work.print_work()
                print("-----")
            print("\n\n")

    def update_work_by_url(self, url: str, name: str = "None", year: int = 0,
                           price: int = 0, size: str = "None",
                           description: str = "None", status: bool = False,
                           img_url: str = "None", img_file_name: str = "None"):
        for categorie, content in self.__works.items():
            for i, work in enumerate(content["list"]):
                if work.get_link() == url:
                    content["list"][i] = Work(
                        link=url, name=name, year=year,
                        size=size, status=status, price=price,
                        description=description, img_url=img_url,
                        img_file_name=img_file_name
                    )
                    return

    def write_works(self):
        file_name = f"[{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}]"
        file_name += "_works_save.txt"
        os.makedirs("works_saves", exist_ok=True)
        with open(f"./works_saves/{file_name}", "a") as f:
            f.write("[CATEGORIES]\n")
            for cate, content in self.__works.items():
                f.write(f"{cate}\n")
            f.write("\n[WORKS]\n")
            for cate, content in self.__works.items():
                for work in content["list"]:
                    f.write("-----\n")
                    f.write(f"name:{work.get_name()}\n")
                    f.write(f"categorie:{cate}\n")
                    f.write(f"link:{work.get_link()}\n")
                    f.write(f"year:{work.get_year()}\n")
                    f.write(f"size:{work.get_size()}\n")
                    f.write(f"status:{work.get_status()}\n")
                    f.write(f"price:{work.get_price()}\n")
                    f.write(f"img_url:{work.get_img_url}")
                    f.write(f"img_file_name:{work.get_img_file_name()}")
                    f.write(f"description:{work.get_description()}\n")
                    f.write("\n")

    # Getters
    def get_links_list(self) -> list[str]:
        links_list = []
        for categorie, content in self.__works.items():
            for work in content["list"]:
                links_list.append(work.get_link())
        return links_list

    def get_imgs_list(self) -> list[dict[str, str]]:
        imgs = []

        for categorie, content in self.__works.items():
            for work in content["list"]:
                imgs.append({
                    "link": work.get_img_url(),
                    "file_name": work.get_img_file_name()
                })
        return imgs


class Work:
    def __init__(self, link: str, name: str, year: int, size: str,
                 status: bool, price: int, description: str, img_url: str,
                 img_file_name: str):
        self.__name = name
        self.__year = year
        self.__size = size
        self.__status = status
        self.__link = link
        self.__price = price
        self.__description = description
        self.__img_url = img_url
        self.__img_file_name = img_file_name

    def print_work(self) -> None:
        print(f"name: {self.__name}")
        print(f"link: {self.__link}")
        print(f"year: {self.__year}")
        print(f"size: {self.__size}")
        print(f"status: {self.__status}")
        print(f"price: {self.__price}")
        print(f"image url: {self.__img_url}")
        print(f"image file: {self.__img_file_name}")
        print(f"description: {self.__description}")

    # Getters
    def get_name(self) -> str:
        return self.__name

    def get_link(self) -> str:
        return self.__link

    def get_year(self) -> int:
        return self.__year

    def get_size(self) -> str:
        return self.__size

    def get_status(self) -> bool:
        return self.__status

    def get_price(self) -> int:
        return self.__price

    def get_description(self) -> str:
        return self.__description

    def get_img_url(self) -> str:
        return self.__img_url

    def get_img_file_name(self) -> str:
        return self.__img_file_name

from typing import Union
from datetime import datetime
import os

from .Errors import DataError


class ParsedData:
    def __init__(self):
        self.__works: dict[str, dict[str, Union[str, list[Work]]]] = {}


    def add_work(self, categorie, link, name="None", year=0,
                 size="None", status="None", price=0, description="None",
                 img_url="None", img_file_name="None") -> None:
        if categorie in self.__works:
            self.__works[categorie]["list"].append(
                Work(link=link, name=name, year=year, size=size, status=status,
                     price=price, description=description, img_url=img_url,
                     img_file_name=img_file_name)
            )
        else:
            raise DataError("No categories created")

    def init_last_registry(self, save_url: str) -> None:
        works_txt = []
        categories = []

        with open(save_url, "r", encoding="utf-8") as f:
            file = f.read()
            cate_part, works_part = file.split("[WORKS]", 1)
            works_txt = works_part.strip().split("-----")
            categories = cate_part.strip().split("\n")
            print("File opened successfully")
        default_values = {
            "categorie": None,
            "link": None,
            "name": None,
            "year": None,
            "size": None,
            "status": False,
            "price": 0,
            "description": None,
            "img_url": None,
            "img_file_name": None
        }
        if categories:
            for categorie in categories:
                self.add_categorie(categorie.strip(), "")

        if works_txt:
            for work_txt in works_txt:
                work_txt_s = work_txt.strip()
                if not work_txt_s:
                    print("no bloc found")
                    continue

                work_datas = default_values.copy()
                lines = work_txt_s.split("\n")
                for line in lines:
                    if ":" in line:
                        key, value = line.split(":", 1)
                        work_datas[key.strip()] = value.strip()
                if work_datas["name"] != None and work_datas["name"] != "None":
                    print("ADDING:", work_datas["name"])
                    self.add_work(
                        categorie=work_datas["categorie"],
                        link=work_datas["link"],
                        name=work_datas["name"],
                        year=work_datas["year"],
                        size=work_datas["size"],
                        status=work_datas["status"],
                        price=work_datas["price"],
                        description=work_datas["description"],
                        img_url=work_datas["img_url"],
                        img_file_name=work_datas["img_file_name"]
                    )
        else:
            print("No work find")

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
                    f.write(f"img_url:{work.get_img_url()}\n")
                    f.write(f"img_file_name:{work.get_img_file_name()}\n")
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

    def get_works_as_list(self) -> list[dict]:
        final_list = []

        for categorie, content in self.__works.items():
            for work in content["list"]:
                work_dict = work.get_work_as_dict()
                work_dict["categorie"] = categorie
                final_list.append(work_dict)
        return final_list
    
    def get_cate_as_list(self) -> list[dict]:
        final_list = []

        for categorie, content in self.__works.items():
            final_list.append({"name": categorie, "description": content["link"]})
        return final_list


class Work:
    def __init__(self, link: str, name: str = "None", year: int = 0,
                 size: str = "None", status: bool = False, price: int = 0,
                 description: str = "None", img_url: str = None,
                 img_file_name: str = "None"):
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
    
    def get_work_as_dict(self) -> dict:
        return {
            "name": self.__name,
            "link": self.__link,
            "year": self.__year,
            "size": self.__size,
            "status": self.__status,
            "price": self.__price,
            "description": self.__description,
            "img_url": self.__img_url,
            "img_file_name": self.__img_file_name
        }

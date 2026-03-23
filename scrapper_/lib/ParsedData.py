from typing import Union


class ParsedData:

    def __init__(self):
        self.__works: dict[str, dict[str, Union[str, list]]] = {}

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

    def get_links_list(self) -> list[str]:
        links_list = []
        for categorie, content in self.__works.items():
            for work in content["list"]:
                links_list.append(work.get_link())
        return links_list

    def update_work_by_url(self, url: str, name: str = "None", year: int = 0,
                           price: int = 0, size: str = "None",
                           description: str = "None", status: bool = False):
        for categorie, content in self.__works.items():
            for i, work in enumerate(content["list"]):
                if work.get_link() == url:
                    content["list"][i] = Work(
                        link=url, name=name, year=year,
                        size=size, status=status, price=price,
                        description=description
                    )
                    break


class Work:
    def __init__(self, link, name="None", year=0, size="None",
                 status="None", price=0, description=""):
        self.__name = name
        self.__year = year
        self.__size = size
        self.__status = status
        self.__link = link
        self.__price = price
        self.__description = description

    def print_work(self) -> None:
        print(f"name: {self.__name}")
        print(f"link: {self.__link}")
        print(f"year: {self.__year}")
        print(f"size: {self.__size}")
        print(f"status: {self.__status}")
        print(f"price: {self.__price}")
        print(f"description: {self.__description}")

    # Getters
    def get_link(self) -> str:
        return self.__link

class ParsedData:

    def __init__(self):
        self.__works = {}

    def add_work(self, categorie, name, link, year = 0, size = "None", status = "None"):
        if categorie in self.__works:
            self.__works[categorie]["list"].append(
                self._Work(name=name, link=link, year=year, size=size, status=status)
            )
    
    def add_categorie(self, name, link):
        if name not in self.__works:
            self.__works[name] = {"link": link, "list": []}
    
    def print_work_list(self):
        for categorie, content in self.__works.items():
            print("========================")
            print(f"- {categorie} ({content['link']}): ")
            for work in content["list"]:
                work.print_work()
                print("-----")
            print("\n\n")


    class _Work:
        def __init__(self, name, link, year = 0, size = "None", status = "None"):
            self.__name = name
            self.__year = year
            self.__size = size
            self.__status = status
            self.__link = link

        def print_work(self):
            print(f"name: {self.__name}")
            print(f"link: {self.__link}")
            # print(f"year: {self.__year}")
            # print(f"size: {self.__size}")
            # print(f"status: {self.__status}")

    
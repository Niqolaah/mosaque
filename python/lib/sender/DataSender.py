import time
import os
from PIL import Image

from ..ParsedData import ParsedData
from ..LogRecorder import LogRecorder, LogType
from .Api import Api
from ..Errors import APIError

class DataSender:
    def __init__(self, works: ParsedData, logs: LogRecorder):
        self.__works = works
        self.__logs = logs
        try:
            self.api = Api(logs)
        except APIError as e:
            raise APIError(e)

    def post_scrapped_works(self):
        dict_works = self.__works.get_works_as_list()
        existing_cate = self.api.get_table_request("categories")
        existing_works = self.api.get_table_request("tableaux")

        for dict_work in dict_works:
            if self.__check_work_data(dict_work):
                if not self.is_work_exist(existing_works, dict_work):
                    time.sleep(0.5)
                    if self.api.post_work_request(
                        name=dict_work["name"],
                        id_categorie=self.get_correponding_cate_id(dict_work["categorie"],
                                                                   existing_cate),
                        price=dict_work["price"],
                        year=dict_work["year"],
                        size=dict_work["size"],
                        status=dict_work["status"],
                        art_majeur_link=dict_work["link"],
                        img_path=dict_work["img_file_name"],
                        description=dict_work["description"]
                        ):
                        self.__logs.add_log(f"Work {dict_work["name"]} has successfuly sent",
                                            LogType.LOGSUCCESS)
                    else:
                        self.__logs.add_log(f"\npost data: incomplete data : {dict_work["name"]}",
                                            LogType.LOGINFO)
                elif len(self.is_work_changed(existing_works, existing_cate, dict_work)) > 0:
                    list_of_changes = self.is_work_changed(existing_works, existing_cate, dict_work)
                    data = {}
                    for change in list_of_changes:
                        data[change] = dict_work[change]
                    data["art_majeur_link"] = dict_work["link"]
                    if self.api.update_work(data):
                        print(f"Work {dict_work['name']} has changed")
                    else :
                        print(f"Error on update {dict_work['name']}: {list_of_changes}")
            else:
                self.__logs.add_log(f"Invalid work: {dict_work['name']}",
                                    LogType.LOGINFO)


    def post_scrapped_categories(self):
        scrapped_cate = self.__works.get_cate_as_list()
        existing_cate = self.api.get_table_request("categories")

        for dict_cate in scrapped_cate:
            time.sleep(0.5)
            if (self.__check_cate_data(dict_cate) and 
                not self.is_categorie_exist(existing_cate, dict_cate["name"])):

                if not self.api.post_categorie_request(
                    name=dict_cate["name"],
                    description="Une description a venir prochainement",
                    img_path="A venir"):

                    self.__logs.add_log(f"post data: incomplete data : {dict_cate["name"]}",
                                        LogType.LOGINFO)


    def is_categorie_exist(self, existing_cate: list[dict], cate_name: str) -> bool:
        return cate_name in [existing["name"] for existing in existing_cate]
    
    def is_work_exist(self, existing_works: list[dict], work_dict: dict) -> bool:
        for existing_work in existing_works:
            if work_dict["link"] ==  existing_work["art_majeur_link"]:
                return True
        return False
    
    def is_work_changed(self, existing_works: list[dict],
                        existing_categories: list[dict], work_dict: dict) -> list[str]:
        for existing_work in existing_works:
            if work_dict["link"] == existing_work["art_majeur_link"]:
                list_of_changes = []
                if (work_dict["name"] != existing_work["name"]):
                    list_of_changes.append("name")
                
                if int(self.get_correponding_cate_id(work_dict["categorie"],
                        existing_categories)) != int(existing_work["id_categorie"]):
                    list_of_changes.append("id_categorie") 

                if float(work_dict["price"]) != float(existing_work["price"]):
                    list_of_changes.append("price")

                if int(work_dict["year"]) != int(existing_work["year"]):
                    list_of_changes.append("year")
                
                if work_dict["size"] != existing_work["size"]:
                    list_of_changes.append("size")

                if work_dict["status"] != existing_work["status"]:
                    list_of_changes.append("status")

                if work_dict["img_file_name"] != existing_work["img_path"]:
                    list_of_changes.append("img_file_name")

                if work_dict["description"] != existing_work["description"]:
                    list_of_changes.append("description")
                
                return list_of_changes
        return False


    def __check_work_data(self, dict_works) -> bool:
        if (dict_works["name"] and dict_works["name"] != "None" and
              int(dict_works["price"]) >= 0 and
            int(dict_works["year"]) >= 2010 and int(dict_works["year"]) <= 2060 and
            dict_works["size"] and dict_works["size"] != "None" and
            dict_works["status"] and dict_works["status"] != "None"and
            dict_works["img_file_name"] and dict_works["img_file_name"] != "None" and
            dict_works["description"] and dict_works["description"] != "None"and
            dict_works["link"] and dict_works["link"] != "None"):
            return True
        return False


    def __check_cate_data(self, cate_data: dict) -> bool:
        if (cate_data["name"] and cate_data["name"] != "None" and
              cate_data["name"] != "[CATEGORIES]"):
            return True
        return False
        
    
    def get_correponding_cate_id(self, cate_name: str, categories: list[dict]) -> int:
        for categorie in categories:
            if cate_name == categorie["name"]:
                return categorie["id_categorie"]
        return -1
    

    def is_valid_image(self, filepath: str) -> bool:
        if not os.path.exists(filepath):
            return False

        if os.path.getsize(filepath) == 0:
            return False
        
        try:
            with Image.open(filepath) as img:
                img.verify()
            return True
        except Exception:
            return False
        
    def send_downloaded_imgs(self):
        for img in [imgs["file_name"] for imgs in self.__works.get_imgs_list()]:
            img_path = f"imgs/{img}"
            if self.is_valid_image(img_path):
                try:
                    self.api.send_image(img_path)
                    os.remove(img_path)
                except Exception:
                    self.__logs.add_log(f"Cannot send image: {img_path}",
                                        LogType.LOGINFO)
        

    
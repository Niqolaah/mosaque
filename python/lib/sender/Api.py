import urllib3
import requests
import paramiko
import os
from dotenv import load_dotenv

from ..LogRecorder import LogRecorder, LogType
from ..Errors import APIError

class Api:
    def __init__(self, logs: LogRecorder):
        self.__logs = logs
        try:
            self.load_env_var()
        except APIError as e:
            raise APIError(e)

    def load_env_var(self):
        load_dotenv()
        self.__hostname = os.getenv('HOSTNAME_DB')
        self.__username = os.getenv('USERNAME_DB')
        self.__key_path = os.getenv('KEY_PATH_SSH')
        # self.__key_path = os.path.expanduser("~/.ssh/o2switch_key")
        self.__password = os.getenv('PASSWORD_DB')
        self.__token = os.getenv('TOKEN_API')
        if (not self.__hostname or \
            not self.__username or \
            not self.__key_path or \
            not self.__password or \
            not self.__token):
            raise APIError("Environment Variable not fount")



    def get_table_request(self, table: str) -> list[dict]:
        url = "https://agnescouret.fr/api/get.php"
        data = {
            "token": self.__token,
            "table": table
        }
        urllib3.disable_warnings()
        response = requests.get(url, params=data, verify=False)
        if response.status_code == 200:
            return response.json()
        return False
    
    def post_categorie_request(self, name: str, description: str, img_path: str) -> bool:
        url = "https://agnescouret.fr/api/insert_categorie.php"
        data = {
            "token": self.__token,
            "name": name,
            "description": description,
            "img_path": img_path
        }
        urllib3.disable_warnings()
        response = requests.post(url, data=data, verify=False)
        if response.status_code == 200:
            return True
        return False
    
    def post_work_request(self, name: str, id_categorie: int, price: int,
                  year: int, size: str, status: bool, img_path: str,
                  art_majeur_link: str, description: str) -> bool:
        url = "https://agnescouret.fr/api/insert_work.php"

        data = {
            "token": self.__token,
            "name": name,
            "id_categorie": id_categorie,
            "price": price,
            "year": year,
            "size": size,
            "status": status,
            "img_path": img_path,
            "art_majeur_link": art_majeur_link,
            "description": description
        }
        urllib3.disable_warnings()
        response = requests.post(url, data=data, verify=False)
        if response.status_code == 200:
            return True
        return False
    
    def del_work_by_link(self, link: str) -> None:
        url = "https://agnescouret.fr/api/del_work.php"
        data ={
            "token": self.__token,
            "art_majeur_link": link
        }
        urllib3.disable_warnings()
        response = requests.post(url, data=data, verify=False)
        if response.status_code == 200 and response.text  == "OK":
            return True
        print(response.text)
        return False
    
    def get_imgs_info(self):
        url = url = "https://agnescouret.fr/api/img_list.php"
        data={"token": self.__token}
        urllib3.disable_warnings()
        response = requests.get(url, params=data, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError(f"Impossible to connect api : {response.text}")

    def send_image(self, local_file: str):
        file_name = local_file.split("/")[-1].strip()
        remote_file = f"public_html/sources/imgs/works/{file_name}"

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(
                hostname=self.__hostname,
                username=self.__username,
                key_filename=os.path.expanduser(self.__key_path),
                password=self.__password
            )
            sftp = ssh.open_sftp()
            try:
                sftp.put(local_file, remote_file)

                self.__logs.add_log(f"Data {file_name} Successfuly sent",
                      LogType.LOGSUCCESS)
            except Exception as e:
                self.__logs.add_log(f"Impossible to send data: {e}",
                      LogType.LOGERROR)
            finally:
                sftp.close()
        except Exception as e:
            self.__logs.add_log(f"Impossible to open ssh: {e}",
                      LogType.LOGERROR)
        finally:
            ssh.close()
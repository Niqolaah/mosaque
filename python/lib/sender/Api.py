import urllib3
import requests
import paramiko
import os

from ..LogRecorder import LogRecorder, LogType

class Api:
    def __init__(self, logs: LogRecorder):
        self.__logs = logs

        self.__hostname = "whisper.o2switch.net"
        self.__username = "coag8475"
        self.__key_path = os.path.expanduser("~/.ssh/o2switch_key")
        self.__password = "tkr3-3Rxk-NdT{"
        self.__token = "iuo89sefjse0fusjflkjij(*lkjfsd89j2E39opkOK090)(*#27"

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
    
    def send_image(self, local_file: str):
        remote_file = "public_html/images/image.jpg"

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(
                hostname=self.__hostname,
                username=self.__username,
                key_filename=self.__key_path,
                password=self.__password
            )
            sftp = ssh.open_sftp()
            try:
                sftp.put(local_file, remote_file)
            except Exception:
                self.__logs.add_log("Impossible to send data",
                      LogType.LOGERROR)
                sftp.close()
        except Exception:
            self.__logs.add_log("Impossible to open ssh",
                      LogType.LOGERROR)
            ssh.close()

        self.__logs.add_log("Data Successfuly sent",
                      LogType.LOGSUCCESS)
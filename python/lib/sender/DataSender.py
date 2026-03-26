import os
import paramiko
import requests
import urllib3
import time

from ..ParsedData import ParsedData
from ..LogRecorder import LogRecorder, LogType

class DataSender:
	def __init__(self, works: ParsedData, logs: LogRecorder):
		self.__works = works
		self.__logs = logs

		self.__hostname = "whisper.o2switch.net"
		self.__username = "coag8475"
		self.__key_path = os.path.expanduser("~/.ssh/o2switch_key")
		self.__password = "tkr3-3Rxk-NdT{"
		self.__token = "iuo89sefjse0fusjflkjij(*lkjfsd89j2E39opkOK090)(*#27"

	def post_scrapped_works(self):
		dict_works = self.__works.get_works_as_list()
		categories = self.get_categories_request("categories")
		print("CAAAAAAAAAAAAAAAAAAAAAAAAAAATEGORIES")
		print(categories)
		for dict_work in dict_works:
			if self.__check_work_data(dict_work):
				time.sleep(0.5)
				if not self.post_work_request(
					name=dict_work["name"],
					id_categorie=self.get_correponding_cate_id(dict_work["categorie"], categories),
					price=dict_work["price"],
					year=dict_work["year"],
					size=dict_work["size"],
					status=dict_work["status"],
					art_majeur_link=dict_work["link"],
					img_path=dict_work["img_file_name"],
					description=dict_work["description"]
				):
					print(f"\npost data: incomplete data : {dict_work}\n")
			else:
				print(f"checkdata: incomplete data : {dict_work}")

	def post_scrapped_categories(self):
		dict_categories = self.__works.get_cate_as_list()
		for dict_cate in dict_categories:
			time.sleep(0.5)
			if self.__check_cate_data(dict_cate):
				if not self.post_categorie_request(
					name=dict_cate["name"],
					# description=dict_cate["description"]
					description="Une description a venir prochainement",
					img_path="A venir"
				):
					print(f"\npost data: incomplete data : {dict_cate}\n")
			else:
				print("Check cate failed")

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
			self.__logs.add_log(f"{name} successfully sent",
					   LogType.LOGSUCCESS)
			print(f"success message: {response.text}")
			return True
		self.__logs.add_log(f"{name} could not be sent: ({response.text}: {response.status_code})",
					LogType.LOGINFO)
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
			self.__logs.add_log(f"{name} successfully sent",
					   LogType.LOGSUCCESS)
			print(f"success message: {response.text}")
			return True
		self.__logs.add_log(f"{name} could not be sent: ({response.text}: {response.status_code})",
					LogType.LOGINFO)
		return False
	
	def get_correponding_cate_id(self, cate_name: str, categories: list[dict]) -> int:

		for categorie in categories:
			if cate_name == categorie["name"]:
				return categorie["id_categorie"]
		return -1

	def get_categories_request(self, table: str) -> list[dict]:
		url = "https://agnescouret.fr/api/get.php"
		data = {
			"token": self.__token,
			"table": table
		}
		urllib3.disable_warnings()
		response = requests.get(url, params=data, verify=False)
		if response.status_code == 200:
			self.__logs.add_log(f"successfully sent",
					   LogType.LOGSUCCESS)
			return response.json()
		self.__logs.add_log(f"could not be sent: ({response.text}: {response.status_code})",
					LogType.LOGINFO)
		return False

	
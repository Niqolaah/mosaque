import os
import paramiko
import requests
import urllib3

class DataSender:
	def __init__(self):


	def send_image(self):
		local_file = "image.jpg"
		remote_file = "public_html/images/image.jpg"

		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		ssh.connect(
			hostname=self.__hostname,
			username=self.__username,
			key_filename=self.__key_path,
			password=self.__password
		)
		try:
			sftp = ssh.open_sftp()
			try:
				sftp.put(local_file, remote_file)
			except Exception:
				sftp.close()
		except Exception:
			ssh.close()

		print("✅ Image envoyée")

		
	def post_request(self, name: str, id_category: int, price: int,
				  year: int, size: str, status: bool, img_link: str,
				  art_majeur_link: str, description: str) -> None:
		url = "https://agnescouret.fr/api/insert.php"

		data = {
			"token": self.__token,
			"name": name,
			"id_category": id_category,
			"price": price,
			"year": year,
			"size": size,
			"status": status,
			"img_link": img_link,
			"art_majeur_link": art_majeur_link,
			"description": description
		}
		urllib3.disable_warnings()
		response = requests.post(url, data=data, verify=False)

		print(response.status_code)
		print(response.text)
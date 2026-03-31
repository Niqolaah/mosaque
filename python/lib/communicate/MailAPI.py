import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..Errors import MailError 

class MailAPI:

	def __init__(self) -> None:
		self.__host = "whisper.o2switch.net"
		self.__port = 465
		self.__user = "scrapper-bot@agnescouret.fr"
		self.__pass = "tkr3-3Rxk-NdT{"

	def send(self, to: str, subject: str, body: str) -> bool:
		try:
			msg = MIMEMultipart()
			msg["From"] = self.__user
			msg["To"] = to
			msg["Subject"] = subject
			msg.attach(MIMEText(body, 'plain'))

			with smtplib.SMTP(self.__host, self.__port) as server:
				server.starttls()
				server.login(self.__user, self.__pass)
				server.sendmail(self.__user, to, msg.as_string())

			return True
		except Exception as e:
			raise MailError(f"Impossible to send mail: {e}")
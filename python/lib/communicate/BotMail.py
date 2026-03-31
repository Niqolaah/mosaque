from .MailAPI import MailAPI


class BotMail:
	def __init__(self):
		self.__api = MailAPI()
	
	def send_mail(self):
		self.__api.send(
			to="ngaubil654@gmail.com",
			subject="Test",
			body="Test envoie mail"
		)

	
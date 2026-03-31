from lib.scrapper_.Scrapper import Scrapper
from lib.Errors import CloudflairError
from lib.LogRecorder import LogRecorder, LogType
from lib.sender.DataSender import DataSender
from lib.ParsedData import ParsedData
from lib.sender.Api import Api
from lib.communicate.BotMail import BotMail




if __name__ == "__main__":
    data = ParsedData()
    logs = LogRecorder(verbose=True)
    api = Api(logs)
    scrapper = Scrapper(logs, data, api)
    mail = BotMail()

    try:
        mail.send_mail()
    except Exception as e:
        print(e)
    # try:
    #     scrapper.scrap(visibility=False)
    #     # data.init_last_registry("works_saves/[31-03-2026_11-01-16]_works_save.txt")
    #     # scrapper.download_imgs(visibility=True)
    #     sender = DataSender(data, logs)
    #     sender.send_downloaded_imgs()
    #     sender.post_scrapped_categories()
    #     sender.post_scrapped_works()
    # except CloudflairError as e:
    #     print(f"Cloudflair Error Detected: {e}")
    # except Exception as e:
    #     logs.add_log(f"Unknow Error: {e}", LogType.LOGERROR)
    # finally:
    #     logs.write_logs()

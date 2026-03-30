from lib.scrapper_.Scrapper import Scrapper
from lib.Errors import CloudflairError
from lib.LogRecorder import LogRecorder, LogType
from lib.sender.DataSender import DataSender
from lib.ParsedData import ParsedData
from lib.sender.Api import Api




if __name__ == "__main__":
    data = ParsedData()
    logs = LogRecorder(verbose=True)
    api = Api(logs)
    scrapper = Scrapper(logs, data, api)

    try:
        scrapper.scrap(visibility=False)
        # data.init_last_registry("works_saves/[27-03-2026_08-26-38]_works_save.txt")
        # scrapper.download_imgs(visibility=True)
        sender = DataSender(data, logs)
        sender.send_downloaded_imgs()
        # sender.post_scrapped_categories()
        # sender.post_scrapped_works()
    except CloudflairError as e:
        print(f"Cloudflair Error Detected: {e}")
    except Exception as e:
        logs.add_log(f"Unknow Error: {e}", LogType.LOGERROR)
    finally:
        logs.write_logs()

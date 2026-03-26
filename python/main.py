from lib.scrapper_.Scrapper import Scrapper
from lib.Errors import CloudflairError
from lib.LogRecorder import LogRecorder, LogType
from lib.sender.DataSender import DataSender
from lib.ParsedData import ParsedData




if __name__ == "__main__":
    data = ParsedData()
    logs = LogRecorder(verbose=True)
    scrapper = Scrapper(logs, data)
    try:
        # scrapper.scrap(visibility=False)
        data.init_last_registry("works_saves/[26-03-2026_09-42-40]_works_save.txt")
    except CloudflairError as e:
        print(f"Cloudflair Error Detected: {e}")
    except Exception as e:
        logs.add_log(f"Unknow Error: {e}", LogType.LOGERROR)
    finally:
        logs.write_logs()

    sender = DataSender(data, logs)
    sender.post_scrapped_categories()
    sender.post_scrapped_works()

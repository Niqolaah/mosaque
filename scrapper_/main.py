from lib.Scrapper import Scrapper
from lib.Errors import CloudflairError
from lib.LogRecorder import LogRecorder, LogType



if __name__ == "__main__":
    logs = LogRecorder(verbose=True)
    scrapper = Scrapper(logs)

    try:
        scrapper.scrap(visibility=False)
    except CloudflairError as e:
        print(f"Cloudflair Error Detected: {e}")
    except Exception as e:
        logs.add_log(f"Unknow Error: {e}", LogType.LOGERROR)
    finally:
        logs.write_logs()

from lib.Scrapper import Scrapper
from lib.Errors import CloudflairError
from lib.LogRecorder import LogRecorder

if __name__ == "__main__":
    logs = LogRecorder(verbose=True)
    scrapper = Scrapper(logs)

    try:
        scrapper.scrap(visibility=False)
    except CloudflairError as e:
        print(f"Error Detected: {e}")
    except Exception as e:
        print(e)
    finally:
        logs.write_logs()

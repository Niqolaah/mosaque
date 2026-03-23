from lib.Scrapper import Scrapper
from lib.Errors import CloudflairError

if __name__ == "__main__":
    scrapper = Scrapper()
    try:
        scrapper.scrap()
    except CloudflairError as e:
        print(f"Error Detected: {e}")

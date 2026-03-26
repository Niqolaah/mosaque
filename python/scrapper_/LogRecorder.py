from datetime import datetime
from enum import Enum


class LogType(Enum):
    LOGERROR = "LOGERROR"
    LOGSUCCESS = "LOGSUCCESS"
    LOGINFO = "LOGINFO"


class LogRecorder:
    def __init__(self, verbose: bool = False):
        self.__verbose = verbose
        self.__logs: dict[LogType, list[str]] = {
            LogType.LOGERROR: [],
            LogType.LOGSUCCESS: [],
            LogType.LOGINFO: []
        }

    def add_log(self, txt: str, logtype: LogType) -> None:
        final_str = f"[{datetime.now().strftime("%d/%m/%Y-%H:%M:%S")}] "
        final_str += txt
        self.__logs[logtype].append(final_str)
        if self.__verbose:
            print(f"{logtype.value}: {final_str}")

    def print_logs(self) -> None:
        for logtype, content in self.__logs.items():
            if content:
                print(f"\n==== {logtype.value} ====")
                for log in content:
                    print(log)

    def write_logs(self) -> None:
        if self.__logs[LogType.LOGINFO]:
            with open("logs_info.txt", "a") as f:
                for log in self.__logs[LogType.LOGINFO]:
                    f.write(f"{log}\n")

        with open("logs_errors.txt", "a") as f:
            if self.__logs[LogType.LOGERROR]:
                for log in self.__logs[LogType.LOGERROR]:
                    f.write(f"{log}\n")


if __name__ == "__main__":
    log = LogRecorder()
    log.add_log("Un LOG", LogType.LOGINFO)
    log.print_logs()

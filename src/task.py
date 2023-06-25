from typing import Union
from dataclasses import dataclass
from datetime import datetime
from time import time, mktime

DATETIME_FORMAT = "%Y/%m/%d %H:%M"


@dataclass
class Task:
    container: str
    temperature: str = '-22.0'
    timestamp: Union[int, str] = int(time()) - 600

    def written(self) -> dict:
        self.timestamp = datetime.strftime(datetime.fromtimestamp(self.timestamp), DATETIME_FORMAT)
        return self.__dict__

    def being_read(self):
        self.timestamp = int(mktime(datetime.strptime(self.timestamp, DATETIME_FORMAT).timetuple()))
        return self

    @staticmethod
    def fieldnames() -> list:
        return list(Task.__annotations__.keys())

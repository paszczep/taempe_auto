from typing import Union
from dataclasses import dataclass
from datetime import datetime
from time import time, mktime

DATETIME_FORMAT = "%Y/%m/%d %H:%M"


@dataclass
class Task:
    container: str
    temperature: str = '0.0'
    timestamp: Union[int, str] = int(time()) - 600

    @property
    def datetime(self) -> str:
        return datetime.strftime(datetime.fromtimestamp(self.timestamp), DATETIME_FORMAT)

    def written(self) -> dict:
        self.timestamp = self.datetime
        return self.__dict__

    def being_read(self):
        self.timestamp = int(mktime(datetime.strptime(self.timestamp, DATETIME_FORMAT).timetuple()))
        return self

    def reported(self) -> str:
        return f'{self.container} {self.datetime} {self.temperature}'

    @staticmethod
    def fieldnames() -> list:
        return list(Task.__annotations__.keys())

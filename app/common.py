from datetime import datetime
from uuid import uuid4
from os import mkdir, path
# cSpell:ignoreRegExp string


HOST = "0.0.0.0"
PORT = 9700

DIR = "data"

TOKEN = "mlorc123"
API_KEY = "3032633365366238626630616338383732346437363835613238613965623030"

MODEL_PATH = "app/static/model/ml_model.keras"


class Filenames:
    FORMAT = "%Hh%Mm%Ss-%d-%m-%Y"

    def __init__(self, filename: str | None) -> None:
        if not filename:
            self.__extension = ".jpg"
        else:
            self.__extension = filename[filename.find("."):]
        self.__handle()

    def __handle(self):
        if not path.exists(DIR):
            mkdir(DIR)
        prefix = datetime.now().strftime(self.FORMAT)
        suffix = str(uuid4()).replace('-', '')
        folder_name = f"{prefix}-{suffix}"
        self.folder_path = f"{DIR}/{folder_name}"
        self.original_path = f"{self.folder_path}/original{self.__extension}"
        self.processed_path = f"{self.folder_path}/processed{self.__extension}"
        self.csv_path = f"{self.folder_path}/words.csv"
        self.text_path = f"{self.folder_path}/text.txt"

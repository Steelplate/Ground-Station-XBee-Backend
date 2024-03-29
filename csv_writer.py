import csv
import datetime
import pathlib
import json
import time

class CSV_Writer:
    def __init__(self):

        date = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        

        self.file = open(f"{pathlib.Path(__file__).parent.resolve()}/Logs/{date}.csv", "w")
        self.csv =  csv.writer(self.file)
        self._has_written_headers = False

    def write(self, data: str) -> None:
        data_json = json.loads(data)

        if not self._has_written_headers:
            header = data_json.keys()
            header.append("internalEpochTime")
            self.csv.writerow(header)
            self._has_written_headers = True

        else:
            data = data_json.values()
            data.append(int(time.time()));
            self.csv.writerow(data_json.values())

        self.file.flush()
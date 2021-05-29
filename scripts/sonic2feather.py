import os
import bz2
import argparse
import pandas as pd

from datetime import datetime, timedelta


class SonicFile(object):

    def __init__(self, file: str):
        self.file = file
        self.bad_lines = 0

    def str2datetime(self, value: str):
        return datetime.strptime(value, "%y%m%d%H%M%S")

    def str2float(self, value: str):
        return float(value) / 100

    def read_line(self, line: str):
        decoded_line = line.decode("unicode_escape")
        splited_line = decoded_line.split()
        try:
            t = self.str2datetime(splited_line[0])
            Vx = self.str2float(splited_line[4])
            Vy = self.str2float(splited_line[7])
            Vz = self.str2float(splited_line[10])
            T = self.str2float(splited_line[13])
            if t == self.t0:
                self.ms += 20
                t += timedelta(milliseconds=self.ms)
            else:
                self.ms = 0
                self.t0 = t
            return {"t": t, "Vx": Vx, "Vy": Vy, "Vz": Vz, "T": T}
        except (IndexError, ValueError):
            self.bad_lines += 1
            return None

    def read(self):
        self.t0 = None
        self.ms = 0
        self.data = []
        if self.file.endswith(".bz2"):
            opener = bz2.open
        else:
            opener = open
        with opener(self.file, "r") as f:
            for line in f:
                data = self.read_line(line)
                if data:
                    self.data.append(data)
        return pd.DataFrame(data=self.data)

    def save_as_feather(self):
        df = self.read()
        base_name = os.path.basename(self.file)
        feather_name = base_name.split(".")[0] + ".feather"
        df.to_feather(feather_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Конвертация sonic-файлов в формат feather")
    parser.add_argument("--files", nargs="+", help="Путь до sonic-файлов")
    args = parser.parse_args()
    
    for file in args.files:
        print(f"{file}", end="\r")
        sonic = SonicFile(file)
        sonic.save_as_feather()
        print(f"{file} ✓ (пропущено строк: {sonic.bad_lines})")

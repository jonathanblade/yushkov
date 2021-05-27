import numpy as np
import pandas as pd

Cp = 1005 # Дж/(кг*К)
Cv = 717  # Дж/(кг*К)
R = 287   # Дж/(кг*К)


class FeatherParser(object):

    def __init__(self):
        self.data = pd.DataFrame()

    def load(self, files, columns):
        data = []
        for file in files:
            data.append(pd.read_feather(file, columns=columns))
        self.data = pd.concat(data, ignore_index=True).set_index("t").sort_index()

    def calc_fluc(self, x, window="10T"):
        mean = x.rolling(window).mean()
        fluc = x - mean
        return fluc

    def calc_KET(self):
        fluc = self.calc_fluc(self.data)
        KET = (fluc["Vx"].pow(2) + fluc["Vy"].pow(2) + fluc["Vz"].pow(2)).div(2)
        KET = KET.rolling("3H").mean()
        KET = KET.resample("T").first()
        return KET

    def calc_dcs(self):
        cs = ((Cp / Cv) * R * (self.data["T"] + 273)).apply(np.sqrt)
        dcs = self.calc_fluc(cs)
        dcs = dcs.rolling("3H").mean()
        dcs = dcs.resample("T").first()
        return dcs

import numpy as np
import pandas as pd

from scipy.signal import welch

Cp = 1005 # Дж/(кг*К)
Cv = 717  # Дж/(кг*К)
R = 287   # Дж/(кг*К)
Fs = 50   # Гц


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

    def welch(self, x):
        index, data = welch(x, fs=Fs)
        return pd.Series(index=index, data=data)

    def calc_dV_spectrum(self):
        fluc = self.calc_fluc(self.data)
        S1 = fluc.between_time("00:00", "00:10").apply(self.welch).sum(axis=1)
        S2 = fluc.between_time("06:00", "06:10").apply(self.welch).sum(axis=1)
        S3 = fluc.between_time("12:00", "12:10").apply(self.welch).sum(axis=1)
        S4 = fluc.between_time("18:00", "18:10").apply(self.welch).sum(axis=1)
        return pd.DataFrame(data={"00:00-00:10": S1, "06:00-06:10": S2, "12:00-12:10": S3, "18:00-18:10": S4})

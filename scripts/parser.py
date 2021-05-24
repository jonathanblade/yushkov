import numpy as np
import pandas as pd

from datetime import timedelta


Cp = 1005 # Дж/(кг*К)
Cv = 717  # Дж/(кг*К)
R = 287   # Дж/(кг*К)


class FeatherParser(object):

    def __init__(self):
        self.data = pd.DataFrame()

    def load(self, files, dt=timedelta(milliseconds=20)):
        for file in files:
            data = pd.read_feather(file).set_index("t")
            if dt != timedelta(milliseconds=20):
                data = data.resample(dt).mean()
            self.data = self.data.append(data)
        self.dt = self.get_dt()

    def get_dt(self):
        t = self.data.index.values
        return (t[1] - t[0]) / np.timedelta64(1, "s")

    def calc_fluctuations(self, series, window="10T"):
        rolling_mean = series.rolling(window).mean()
        fluctuations = series - rolling_mean
        return fluctuations.dropna()

    def calc_KET(self):
        dVx = self.calc_fluctuations(self.data["Vx"])
        dVy = self.calc_fluctuations(self.data["Vy"])
        dVz = self.calc_fluctuations(self.data["Vz"])
        KET = (dVx**2 + dVy**2 + dVz**2) / 2
        return KET.to_frame(name="КЭТ")

    def calc_V_spectrum(self):
        S = pd.DataFrame()
        S["f"] = np.fft.rfftfreq(self.data.index.size, self.dt)
        S["Vx"] = np.abs(np.fft.rfft(self.data["Vx"]))
        S["Vy"] = np.abs(np.fft.rfft(self.data["Vy"]))
        S["Vz"] = np.abs(np.fft.rfft(self.data["Vz"]))
        return S.set_index("f")

    def calc_dV_spectrum(self):
        S = pd.DataFrame()
        dVx = self.calc_fluctuations(self.data["Vx"])
        dVy = self.calc_fluctuations(self.data["Vy"])
        dVz = self.calc_fluctuations(self.data["Vz"])
        S["f"] = np.fft.rfftfreq(dVx.index.size, self.dt)
        S["dVx"] = np.abs(np.fft.rfft(dVx))
        S["dVy"] = np.abs(np.fft.rfft(dVy))
        S["dVz"] = np.abs(np.fft.rfft(dVz))
        return S.set_index("f")

    def calc_APE(self, window):
        APE = Cp * (self.data["T"] + 273).rolling(window).std()
        return APE.to_frame(name="ДПЭ")

    def calc_dcs_spectrum(self):
        S = pd.DataFrame()
        cs = np.sqrt((Cp / Cv) * R * (self.data["T"] + 273))
        dcs = self.calc_fluctuations(cs)
        S["f"] = np.fft.rfftfreq(dcs.index.size, self.dt)
        S["dcs"] = np.abs(np.fft.rfft(dcs))
        return S.set_index("f")

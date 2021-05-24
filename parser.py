import pandas as pd

from datetime import timedelta


class FeatherParser(object):

    def __init__(self):
        self.data = pd.DataFrame(columns=["Vx", "Vy", "Vz", "T"])

    def load(self, files: list[str], dt: timedelta):
        for file in files:
            data = pd.read_feather(file).set_index("t").resample(dt).mean()
            self.data = self.data.append(data)

    def calc_fluctuations(self, param: str, window: int):
        rolling_mean = self.data[param].rolling(window).mean()
        fluctuations = self.data[param] - rolling_mean
        return fluctuations

    def calc_KET(self, window: int):
        dVx = self.calc_fluctuations("Vx", window)
        dVy = self.calc_fluctuations("Vx", window)
        dVz = self.calc_fluctuations("Vz", window)
        KET = (dVx**2 + dVy**2 + dVz**2) / 2
        return KET.to_frame(name="КЭТ")

    def calc_cs(self, cp=1006, cv=717, R=1.2):
        cs2 = (cp / cv) * R * (self.data["T"] + 273)

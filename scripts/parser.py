import numpy as np
import pandas as pd

from scipy.signal import welch
from datetime  import datetime, timedelta

from consts import *


class FeatherParser(object):

    def __init__(self):
        self.data = {
            "КЭТ": pd.DataFrame(),
            "Скорость диссипации флуктуаций скорости ветра": pd.DataFrame(),
            "Скорость диссипации флуктуаций скорости звука": pd.DataFrame(),
            "Дисперсия флуктуаций скорости ветра": pd.DataFrame(),
            "Дисперсия флуктуаций скорости звука": pd.DataFrame(),
            "Флуктуации скорости звука": pd.DataFrame(),
            "Флуктуации скорости ветра": pd.DataFrame()
        }

    def welch(self, x):
        index, data = welch(x, fs=Fs)
        return pd.Series(index=index, data=data).rename_axis("f")

    def process(self, file, columns=None):
        file_data = pd.read_feather(file, columns=columns).set_index("t")
        window_left = file_data.index[0]
        window_right = window_left + timedelta(minutes=10)
        result = {
            "КЭТ": [],
            "Скорость диссипации флуктуаций скорости ветра": [],
            "Скорость диссипации флуктуаций скорости звука": [],
            "Дисперсия флуктуаций скорости ветра": [],
            "Дисперсия флуктуаций скорости звука": [],
            "Флуктуации скорости звука": [],
            "Флуктуации скорости ветра": []
        }
        t = []
        while window_right <= file_data.index[-1]:
            t.append(window_left + (window_right - window_left) / 2)
            # Данные за 10 минут
            window_data = file_data.loc[window_left:window_right]
            # Температура
            T = window_data["T"].to_frame()
            # Компоненты скорости ветра
            Vi = window_data.drop("T", axis=1)
            # Скорость звука
            Cs = ((Cp / Cv) * R * (T + 273)).apply(np.sqrt).rename(columns={"T": "Скорость звука"})
            # Флуктуации скорости звука
            dCs = (Cs - Cs.mean()).rename(columns={"Скорость звука": "Флуктуации скорости звука"})
            result["Флуктуации скорости звука"].append(dCs)
            # Флуктуации компонент скорости ветра
            dVi = Vi - Vi.mean()
            # Флуктуации скорости ветра
            dV = dVi.pow(2).sum(axis=1).apply(np.sqrt).to_frame("Флуктуации скорости ветра")
            result["Флуктуации скорости ветра"].append(dV)
            # Средняя скорость ветра
            U = np.sqrt((Vi.mean()**2).sum())
            # Дисперсия флуктуаций скорости ветра
            sigma2_dV = dVi.pow(2).mean().sum()
            result["Дисперсия флуктуаций скорости ветра"].append(sigma2_dV)
            # Дисперсия флуктуаций скорости звука
            sigma2_dCs = float(dCs.pow(2).mean())
            result["Дисперсия флуктуаций скорости звука"].append(sigma2_dCs)
            # Кинетическая энергия турбулентности (КЭТ)
            KET = dVi.pow(2).sum(axis=1).div(2).to_frame("КЭТ")
            result["КЭТ"].append(KET)
            # Спектральная плотность можности флуктуаций скорости звука
            SdCs = dCs.apply(self.welch).rename(columns={"Флуктуации скорости звука": "Спектральная плотность можности флуктуаций скорости звука"})
            # Спектральная плотность мощности флуктуаций скорости ветра 
            SdV = dVi.apply(self.welch).sum(axis=1).to_frame("Спектральная плотность мощности флуктуаций скорости ветра")
            # Скорость диссипации флуктуаций скорости ветра
            # epsV = 2 * np.pi * SdV**1.5 * SdV.index**2.5 / (Kv**1.5 * u)
            # Отношение скорости диссипации флуктуаций скорости звука к скорости диссипации флуктуаций скорости ветра
            # epsdCs_epsdV = (Kcs / Kv) * SdCs.div(SdV, axis=1).mean()
            window_left = window_right
            window_right += timedelta(minutes=10)
        
        self.data["КЭТ"] = self.data["КЭТ"].append(pd.concat(result["КЭТ"]).resample("T").first())
        
        self.data["Флуктуации скорости звука"] = self.data["Флуктуации скорости звука"].append(pd.concat(result["Флуктуации скорости звука"]).resample("T").first())

        self.data["Флуктуации скорости ветра"] = self.data["Флуктуации скорости ветра"].append(pd.concat(result["Флуктуации скорости ветра"]).resample("T").first())
        
        self.data["Дисперсия флуктуаций скорости ветра"] = self.data["Дисперсия флуктуаций скорости ветра"].append(pd.DataFrame(index=t, data={"Дисперсия флуктуаций скорости ветра": result["Дисперсия флуктуаций скорости ветра"]})
                                                                                                                   .rename_axis("t"))
        
        self.data["Дисперсия флуктуаций скорости звука"] = self.data["Дисперсия флуктуаций скорости звука"].append(pd.DataFrame(index=t, data={"Дисперсия флуктуаций скорости звука": result["Дисперсия флуктуаций скорости звука"]})
                                                                                                                   .rename_axis("t"))

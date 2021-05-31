import numpy as np
import pandas as pd

from scipy.signal import welch
from scipy.optimize import curve_fit
from datetime  import datetime, timedelta

from consts import *


class FeatherParser(object):

    def __init__(self):
        self.data = {
            "КЭТ": [],
            "Скорость диссипации флуктуаций скорости ветра": [],
            "Скорость диссипации флуктуаций скорости звука": [],
            "Дисперсия флуктуаций скорости ветра": [],
            "Дисперсия флуктуаций скорости звука": [],
            "Флуктуации скорости звука": [],
            "Флуктуации скорости ветра": [],
            "Спектр флуктуаций скорости ветра": [],
            "Спектр флуктуаций скорости звука": [],
            "Скорость диссипации кинетической энергии": [],
            "Скорость диссипации флуктуаций скорости звука": []
        }

    def welch(self, x):
        index, data = welch(x, fs=Fs, nperseg=3000)
        return pd.Series(index=index, data=data).rename_axis("f")

    def linear_func(self, x, a, b):
        return a * x + b

    def process(self, file, columns=None):
        file_data = pd.read_feather(file, columns=columns).set_index("t")
        window_left = file_data.index[0]
        window_right = window_left + timedelta(minutes=10)
        while window_right <= file_data.index[-1]:
            t = window_left + (window_right - window_left) / 2
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
            self.data["Флуктуации скорости звука"].append(dCs.resample("T").first())
            # Флуктуации компонент скорости ветра
            dVi = Vi - Vi.mean()
            # Флуктуации скорости ветра
            dV = dVi.pow(2).sum(axis=1).apply(np.sqrt).to_frame("Флуктуации скорости ветра")
            self.data["Флуктуации скорости ветра"].append(dV.resample("T").first())
            # Средняя скорость ветра
            U = np.sqrt((Vi.mean()**2).sum())
            # Дисперсия флуктуаций скорости ветра
            sigma2V = dVi.pow(2).mean().sum()
            self.data["Дисперсия флуктуаций скорости ветра"].append(pd.DataFrame(index=[t], data={"Дисперсия флуктуаций скорости ветра": [sigma2V]}).rename_axis("t"))
            # Дисперсия флуктуаций скорости звука
            sigma2Cs = float(dCs.pow(2).mean())
            self.data["Дисперсия флуктуаций скорости звука"].append(pd.DataFrame(index=[t], data={"Дисперсия флуктуаций скорости звука": [sigma2Cs]}).rename_axis("t"))
            # Кинетическая энергия турбулентности (КЭТ)
            KET = dVi.pow(2).sum(axis=1).div(2).to_frame("КЭТ")
            self.data["КЭТ"].append(KET.resample("T").first())
            # Спектральная плотность мощности флуктуаций скорости звука
            SdCs = dCs.apply(self.welch).rename(columns={"Флуктуации скорости звука": "Спектр флуктуаций скорости звука"})
            self.data["Спектр флуктуаций скорости звука"].append(SdCs)
            # Спектральная плотность мощности флуктуаций скорости ветра 
            SdV = dVi.apply(self.welch).sum(axis=1).to_frame("Спектр флуктуаций скорости ветра")
            self.data["Спектр флуктуаций скорости ветра"].append(SdV)
            try:
                # Выбираем линейный интервал в спектре (всё, что больше 3 Гц)
                mask = np.where(SdV.index.values >= 3)
                popt, pcov = curve_fit(self.linear_func, SdV.index.values[mask]**(-5/3), SdV["Спектр флуктуаций скорости ветра"].values[mask])
                # Скорость дисспации кинетеческой энергии 
                epsV = (popt[0] / Kv)**1.5 * 2 * np.pi / U
                self.data["Скорость диссипации кинетической энергии"].append(pd.DataFrame(index=[t], data={"Скорость диссипации кинетической энергии": [epsV]}).rename_axis("t"))
                # Выбираем линейный интервал в спектре (интервал от 0.1 Гц до 1 Гц)
                mask = np.where((SdCs.index.values >= 0.1) & (SdCs.index.values <= 1))
                popt, pcov = curve_fit(self.linear_func, SdCs.index.values[mask]**(-5/3), SdCs["Спектр флуктуаций скорости звука"].values[mask])
                # Скорость дисспации флуктуаций скорости звука 
                epsCs = (popt[0] / Kcs) * (2 * np.pi / U)**(2/3) * epsV**(1/3)
                self.data["Скорость диссипации флуктуаций скорости звука"].append(pd.DataFrame(index=[t], data={"Скорость диссипации флуктуаций скорости звука": [epsCs]}).rename_axis("t"))
            except (ValueError, TypeError):
                pass
            window_left = window_right
            window_right += timedelta(minutes=10)

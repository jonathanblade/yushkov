import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from parser import FeatherParser


plt.style.use("classic")
plt.rcParams["figure.figsize"] = (19.2, 10.8)
plt.rcParams["figure.dpi"] = 300
plt.rcParams["font.size"] = 20
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["grid.linestyle"] = "dotted"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Построение отношения скоростей диссипации")
    parser.add_argument("--files", nargs="+", help="Пути до feather-файлов")
    args = parser.parse_args()
    
    parser = FeatherParser()
    for file in args.files:
        print(f"{file}", end="\r")
        parser.process(file)
        print(f"{file} ✓")

    epsV = pd.concat(parser.data["Скорость диссипации кинетической энергии"]).rename(columns={"Скорость диссипации кинетической энергии": r"$\varepsilon_{V}$"})
    epsCs = pd.concat(parser.data["Скорость диссипации флуктуаций скорости звука"]).rename(columns={"Скорость диссипации флуктуаций скорости звука": r"$\varepsilon_{Cs}$"})
    sigma2Cs = pd.concat(parser.data["Дисперсия флуктуаций скорости звука"]).rename(columns={"Дисперсия флуктуаций скорости звука": r"$\sigma^2_{Cs}$"})
    sigma2V = pd.concat(parser.data["Дисперсия флуктуаций скорости ветра"]).rename(columns={"Дисперсия флуктуаций скорости ветра": r"$\sigma^2_{V}$"})
    
    sigma3Cs = sigma2Cs.pow(1.5).rename(columns={r"$\sigma^2_{Cs}$": r"$\sigma^3_{Cs}$"})
    sigma3V = sigma2V.pow(1.5).rename(columns={r"$\sigma^2_{V}$": r"$\sigma^3_{V}$"})
    
    epsCs_epsV = (epsCs[r"$\varepsilon_{Cs}$"] / (4 * np.pi * np.pi * epsV[r"$\varepsilon_{V}$"])).to_frame(r"$\varepsilon_{Cs}/4\pi^2\varepsilon_{V}$")
    sigma3Cs_sigma3V = (sigma3Cs[r"$\sigma^3_{Cs}$"] / sigma3V[r"$\sigma^3_{V}$"]).to_frame(r"$\sigma^3_{Cs}/\sigma^3_{V}$")

    plot_data = pd.concat([epsCs_epsV, sigma3Cs_sigma3V]).sort_index().rolling("3H").mean()

    plot = plot_data.plot(grid=True, logy=True)
    
    figure = plot.get_figure()
    figure.savefig("Кубы.png")

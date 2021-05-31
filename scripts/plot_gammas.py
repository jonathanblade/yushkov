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
    parser = argparse.ArgumentParser(description="Построение зависимости вида sigma^2_Cs = gamma * Epsilon_Cs / (4 * pi^2)")
    parser.add_argument("--files", nargs="+", help="Пути до feather-файлов")
    args = parser.parse_args()
    
    parser = FeatherParser()
    for file in args.files:
        print(f"{file}", end="\r")
        parser.process(file)
        print(f"{file} ✓")

    epsCs = pd.concat(parser.data["Скорость диссипации флуктуаций скорости звука"]).rename(columns={"Скорость диссипации флуктуаций скорости звука": r"$\varepsilon_{Cs}$"})
    sigma2Cs = pd.concat(parser.data["Дисперсия флуктуаций скорости звука"]).rename(columns={"Дисперсия флуктуаций скорости звука": r"$\sigma^2_{Cs}$"})
    sigma4Cs = sigma2Cs.pow(2).rename(columns={r"$\sigma^2_{Cs}$": r"$\sigma^4_{Cs}$"})

    gamma1 = (epsCs * 1 / (4 * np.pi * np.pi)).rename(columns={r"$\varepsilon_{Cs}$": r"$\gamma\varepsilon_{Cs}/4\pi^2, \gamma=1$"})
    gamma5 = (epsCs * 5 / (4 * np.pi * np.pi)).rename(columns={r"$\varepsilon_{Cs}$": r"$\gamma\varepsilon_{Cs}/4\pi^2, \gamma=5$"})
    gamma10 = (epsCs * 10 / (4 * np.pi * np.pi)).rename(columns={r"$\varepsilon_{Cs}$": r"$\gamma\varepsilon_{Cs}/4\pi^2, \gamma=10$"})
    
    plot_data = pd.concat([gamma1, gamma5, gamma10, sigma4Cs]).sort_index().rolling("3H").mean()

    plot = plot_data.plot(grid=True, logy=True)
    
    figure = plot.get_figure()
    figure.savefig("Гаммаы.png")

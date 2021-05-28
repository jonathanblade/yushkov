import argparse
import matplotlib.pyplot as plt

from parser import FeatherParser

plt.style.use("classic")
plt.rcParams["figure.figsize"] = (19.2, 10.8)
plt.rcParams["figure.dpi"] = 300
plt.rcParams["font.size"] = 20
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["grid.linestyle"] = "dotted"
plt.rcParams["axes.grid"] = True
plt.rcParams["axes.grid.which"] = "both"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Построение спектра флуктуаций скорости ветра")
    parser.add_argument("--file", help="Путь до feather-файла")
    args = parser.parse_args()
    
    parser = FeatherParser()
    parser.load(args.file, ["t", "Vx", "Vy", "Vz"])

    S = parser.calc_dV_spectrum()
    
    plot = S.plot(loglog=True)
    plot.set_xlabel("$f, Гц$")
    plot.set_ylabel("$S_{V_{*}}$")
    
    figure = plot.get_figure()
    figure.savefig("Спектр_флуктуаций_скорости_ветра.png")

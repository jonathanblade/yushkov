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
    parser = argparse.ArgumentParser(description="Построение флуктуаций скорости звука")
    parser.add_argument("--files", nargs="+", help="Путь до feather-файлов")
    args = parser.parse_args()
    
    parser = FeatherParser()
    parser.load(args.files, ["t", "T"])

    dcs = parser.calc_dcs()
    
    plot = dcs.plot()
    plot.set_xlabel("$t$")
    plot.set_ylabel("$cs_{*}, м/с$")
    
    figure = plot.get_figure()
    figure.savefig("Флуктуации_скорости_звука.png")

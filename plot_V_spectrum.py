import argparse
import matplotlib.pyplot as plt

from parser import FeatherParser

plt.rcParams["figure.figsize"] = (19.2, 10.8)
plt.rcParams["figure.dpi"] = 300
plt.rcParams["font.size"] = 18
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["grid.linestyle"] = "dotted"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Построение графика cпектра скорости ветра")
    parser.add_argument("--files", nargs="+", help="Пути до feather-файлов")
    args = parser.parse_args()
    
    parser = FeatherParser()
    parser.load(args.files)

    S = parser.calc_V_spectrum()

    plot = S.plot(grid=True, loglog=True)
    figure = plot.get_figure()
    figure.savefig("V_spectrum.png")

import argparse
import matplotlib.pyplot as plt

from parser import FeatherParser

plt.rcParams["figure.figsize"] = (19.2, 10.8)
plt.rcParams["figure.dpi"] = 300
plt.rcParams["font.size"] = 18
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["grid.linestyle"] = "dotted"


WINDOW = 10*60*50 # 10 минут


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Построение графика cпектра флуктуаций скорости звука")
    parser.add_argument("--files", nargs="+", help="Пути до feather-файлов")
    args = parser.parse_args()
    
    parser = FeatherParser()
    parser.load(args.files)

    S = parser.calc_dcs_spectrum(WINDOW)

    plot = S.plot(grid=True, loglog=True)
    figure = plot.get_figure()
    figure.savefig("dcs_spectrum.png")

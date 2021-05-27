import argparse
import matplotlib.pyplot as plt

from parser import FeatherParser

plt.style.use("classic")
plt.rcParams["figure.figsize"] = (19.2, 10.8)
plt.rcParams["figure.dpi"] = 300
plt.rcParams["font.size"] = 20
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["grid.linestyle"] = "dotted"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Построение графика исходных данных (компонент скорости ветра и температуры)")
    parser.add_argument("--files", nargs="+", help="Путь до feather-файлов")
    args = parser.parse_args()
    
    parser = FeatherParser()
    parser.load(args.files)

    plot = parser.data.plot(grid=True, secondary_y=["T"])
    figure = plot.get_figure()
    figure.savefig("Исходные_данные.png")

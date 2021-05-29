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
    parser = argparse.ArgumentParser(description="Построение кинетической энергии турбулентности (КЭТ)")
    parser.add_argument("--files", nargs="+", help="Пути до feather-файлов")
    args = parser.parse_args()
    
    parser = FeatherParser()
    for file in args.files:
        print(f"{file}", end="\r")
        parser.process(file)
        print(f"{file} ✓")

    data = parser.data["КЭТ"].rolling("3H").mean()

    plot = data.plot(grid=True, logy=True, legend=False)
    plot.set_xlabel("$t$")
    plot.set_ylabel("$КЭТ, Дж/кг$")
    
    figure = plot.get_figure()
    figure.savefig("КЭТ.png")

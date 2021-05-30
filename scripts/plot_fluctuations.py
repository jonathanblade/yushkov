import argparse
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
    parser = argparse.ArgumentParser(description="Построение флуктуаций скорости ветра и скорости звука")
    parser.add_argument("--files", nargs="+", help="Пути до feather-файлов")
    args = parser.parse_args()
    
    parser = FeatherParser()
    for file in args.files:
        print(f"{file}", end="\r")
        parser.process(file)
        print(f"{file} ✓")

    plot_data = pd.concat([
        pd.concat(parser.data["Флуктуации скорости звука"]).rename(columns={"Флуктуации скорости звука": "$Cs_{*}, м/с$"})
        pd.concat(parser.data["Флуктуации скорости ветра"]).rename(columns={"Флуктуации скорости ветра": "$V_{*}, м/с$"})
    ]).sort_index().rolling("3H").mean()

    plot = plot_data.plot(grid=True, secondary_y="$Cs_{*}, м/с$")
    
    figure = plot.get_figure()
    figure.savefig("Флуктуации_скоростей.png")

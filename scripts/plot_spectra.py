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
    parser = argparse.ArgumentParser(description="Построение локальных спектров флуктуаций скорости ветра и скорости звука")
    parser.add_argument("--file", help="Путь до feather-файла")
    args = parser.parse_args()
    
    parser = FeatherParser()
    print(f"{args.file}", end="\r")
    parser.process(args.file)
    print(f"{args.file} ✓")

    plot_data = pd.concat([
        parser.data["Спектр флуктуаций скорости звука"][0].rename(columns={"Спектр флуктуаций скорости звука": r"$\~Cs (00:00-00:10)$"}),
        parser.data["Спектр флуктуаций скорости звука"][36].rename(columns={"Спектр флуктуаций скорости звука": r"$\~Cs (06:00-06:10)$"}), 
        parser.data["Спектр флуктуаций скорости звука"][72].rename(columns={"Спектр флуктуаций скорости звука": r"$\~Cs (12:00-12:10)$"}),
        parser.data["Спектр флуктуаций скорости звука"][108].rename(columns={"Спектр флуктуаций скорости звука": r"$\~Cs (18:00-18:10)$"}),
        parser.data["Спектр флуктуаций скорости ветра"][0].rename(columns={"Спектр флуктуаций скорости ветра": r"$\~V (00:00-00:10)$"}),
        parser.data["Спектр флуктуаций скорости ветра"][36].rename(columns={"Спектр флуктуаций скорости ветра": r"$\~V (06:00-06:10)$"}), 
        parser.data["Спектр флуктуаций скорости ветра"][72].rename(columns={"Спектр флуктуаций скорости ветра": r"$\~V (12:00-12:10)$"}),
        parser.data["Спектр флуктуаций скорости ветра"][108].rename(columns={"Спектр флуктуаций скорости ветра": r"$\~V (18:00-18:10)$"})
    ])
                 
    plot = plot_data.plot(grid=True, loglog=True)
    
    figure = plot.get_figure()
    figure.savefig("Спектры_флуктуаций.png")

# Usage: python plot_KET.py --files path/to/file1 path/to/file2 path/to/file3
#        python plot_KET.py --files path/to/folder/*
import argparse
import matplotlib.pyplot as plt

from datetime import timedelta

from parser import FeatherParser

plt.rcParams["figure.figsize"] = (19.2, 10.8)
plt.rcParams["figure.dpi"] = 300
plt.rcParams["font.size"] = 18
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["grid.linestyle"] = "dotted"


DT = timedelta(minutes=1) # [мин]
WINDOW_1 = 10             # [мин]
WINDOW_2 = 180            # [мин]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Построение графика кинетической энергии турбулентности (КЭТ)")
    parser.add_argument("--files", nargs="+", help="Пути до feather-файлов")
    args = parser.parse_args()
    
    parser = FeatherParser()
    # Загружаем данные и семплируем их до минутных
    parser.load(args.files, DT)

    # Рассчитываем КЭТ с окном 10 минут, затем сглаживаем его окном 3 часа
    KET = parser.calc_KET(WINDOW_1).rolling(WINDOW_2).mean()
    
    plot = KET.plot(grid=True)
    figure = plot.get_figure()
    figure.savefig("КЭТ.png")

# Турбулентность атмосферы в пограничном слое

## Подготовка
Перед использованием скриптов нужно установить необходимые зависимости. 
Проще всего это можно сделать при помощи [poetry](https://python-poetry.org). 
Устанавливаем poetry, прописываем `poetry config settings.virtualenvs.in-project true` и выполняем:
```bash
$ poetry install
``` 

Далее загружаем вирутальную среду:
```bash
$ poetry shell
```

## Предобработка файлов
Для начала необходимо предобработать "сырые" Юшковские sonic-файлы. 
Для этого есть скрипт `sonic2feather.py`.
После его выполнения на выходе будем иметь файлы с расширением `.feather`, чтение которых занимает гораздо меньше времени.
Пример:
```
$ python sonic2feather.py --files MSU_210201.dat.bz2 MSU_210202.dat.bz2
```

## Построение графиков
> По умолчанию для [расчёта флуктуаций](https://github.com/jonathanblade/yushkov/blob/master/scripts/parser.py#L38) используется окно 10 минут.
```bash
plot_epsilons.py       Отношение скоростей диссипации
plot_fluctuations.py   Флуктуации скорости ветра и скорости звука
plot_gammas.py         Зависимость вида sigma^2_Cs = gamma * Epsilon_Cs / (4 * pi^2)
plot_KET.py            Кинетическая энергия турбулентности
plot_spectra.py        Локальные спектры флуктуаций скорости ветра и скорости звука
```
Пример:
```bash
$ python plot_KET.py --files MSU_210201.feather MSU_210202.feather
```

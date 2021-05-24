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
$ source .venv/bin/activate
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
> По умолчанию для [расчёта флуктуаций](https://github.com/jonathanblade/yushkov/blob/master/scripts/parser.py#L29-L32) используется окно 10 минут.
```bash
plot_dsc_spectrum.py   Спектр флуктуаций скорости звука
plot_dV_spectrum.py    Спектр флуктуаций скорости ветра
plot_KET.py            Кинетическая энергия турбулентности
plot_V_spectrum.py     Спектр скорости ветра
```
Пример:
```bash
$ python plot_KET.py --files MSU_210201.feather MSU_210202.feather
```
Если не хватает памяти для загрузки полного датафрейма, можно просемплировать данные:
```python
parser = FeatherParser()
dt = datetime.timedelta(minutes=1)
parser.load(args.files, dt)
```

import csv
from pathlib import Path
from modules.db_util import put_data


def load_data() -> None:
    """
    Iterates through csv files in /data/ folder
    and adds data from them in redis with filename as the key
    and value as dict.
    """
    directory = '../data'
    files = Path(directory).glob('*.csv')
    for csv_file in files:
        data_to_save = {}
        with open(csv_file, 'r', encoding='UTF-8') as data:
            reader = csv.reader(data, delimiter=',')
            for row in reader:
                data_to_save.update({row[0]: row[1]})
        key = csv_file.stem
        put_data(data_to_save, 0, key)


if __name__ == '__main__':
    load_data()

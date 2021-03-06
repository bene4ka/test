import logging
import os
import sys

# Смотрит, есть ли уже каталог для логгирования, и нет ли файла с именем log.
# Если каталога нет, создает его. Если есть - пишет ошибку в консоль о невозможности создать каталог.
try:
    os.makedirs('log', exist_ok=True)
except FileExistsError:
    print('There is a file with name \'log\' already exists!')

# Инициализируем логгер с именем app.main
logger = logging.getLogger('app.main')

# Задаем требуемое форматирование
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s : %(message)s ")

# Пробуем писать лог, используем заданный формат лога.
# Если сущуествует каталог с именем client.log, то выдаем в консоль ошибку о невозможности создать файл.
try:
    fh = logging.FileHandler('log/client.log', encoding='utf-8')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
except PermissionError:
    print('There is a directory with name \'client.log\' already exists in \'log\' catalogue!')
    sys.exit()
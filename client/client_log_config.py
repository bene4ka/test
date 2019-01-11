import logging
import os
import sys

path = 'log'

try:
    os.makedirs(path, exist_ok=True)
except FileExistsError:
    print('There is a file with name \"{}\" already exists!'.format(path))

logger = logging.getLogger('app.main')

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")
try:
    fh = logging.FileHandler(path + '/server.log', encoding='utf-8')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
except PermissionError:
    print('There is a directory with name \"server.log\" already exists!'.format(path))
    sys.exit()

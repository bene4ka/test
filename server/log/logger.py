import logging

logger = logging.getLogger('app.main')

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")

fh = logging.FileHandler("server.log", encoding='utf-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)


# Добавляем в логгер новый обработчик событий и устанавливаем уровень логирования
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # Создаем потоковый обработчик логирования (по умолчанию sys.stderr):
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.info('Тестовый запуск логирования')

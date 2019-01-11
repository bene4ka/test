# Серверная часть

import sys
import json
import argparse
from socket import *
import logging
import server_log_config

logger = logging.getLogger('app.main')


def arguments():
    """
    Принимает аргументы командной строки [p, n, v], где:
    p - порт, по которому будет работать серверный процесс. По умолчанию равен 7777.
    a - адрес интерфейса, на который будет совершен бинд. По умолчанию пуст, что означает бинд на все интерфейсы.
    v - уровень логгирования (0=NOTSET, 1=DEBUG, 2=INFO 3=WARNING 4=ERROR 5=CRITICAL), по-умолчанию 2.
    :return: лист, где первым элементом является порт, а вторым - IP для прослушки.
    """
    # Инициализация парсера.
    parser = argparse.ArgumentParser(description='Collect options.')
    # Описание доступных опций запуска.
    parser.add_argument('-p', default='7777', help='port', type=int)
    parser.add_argument('-a', default='', help='address', type=str)
    parser.add_argument('-v', default=2, help='verbose level', type=int)
    # Получаем список спарсеных опций.
    parsed_opts = parser.parse_args()
    # Получаем порт и адрес
    port = parsed_opts.p
    address = parsed_opts.a
    # Проверяем уровень логгирования.
    if parsed_opts.v == 0:
        logger.setLevel(logging.NOTSET)
    elif parsed_opts.v == 1:
        logger.setLevel(logging.DEBUG)
    elif parsed_opts.v == 2:
        logger.setLevel(logging.INFO)
    elif parsed_opts.v == 3:
        logger.setLevel(logging.WARNING)
    elif parsed_opts.v == 4:
        logger.setLevel(logging.ERROR)
    elif parsed_opts.v >= 5:
        logger.setLevel(logging.CRITICAL)
    else:
        # Если уровень логгирования выбран неверно, выводим сообщение и глушим сервер.
        logger.setLevel(logging.CRITICAL)
        logger.critical("UNEXPLAINED COUNT IN VERBOSITY LEVEL!")
        print("UNEXPLAINED COUNT IN VERBOSITY LEVEL!")
        sys.exit()
    log_message = 'Будем пробовать запуститься с портом ' + str(port) + \
                  (' на всех интерфейсах.' if address == '' else 'на интерфейсе' + address + '.')
    logger.info(log_message)
    # Возврат листа [порт, адрес]
    return [port, address]


def sock_bind(args):
    """"
    Создает TCP-сокет и присваает порт и интерфейс, полученный из функции arguments()
    :param args: лист из порта в integer и адреса интерфейса в string.
    """
    s = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP.
    logger.info('Открыт сокет.')
    try:
        s.bind((args[1], args[0]))  # Присваивает порт 8888.
        logger.info('Удачно забиндились на порт и интерфейс.')
    except OSError:
        logger.error('Выбранный порт уже занят.')
    s.listen(5)  # Переходит в режим ожидания запросов, одновременно не болеее 5 запросов.
    logger.info('Перешли в режим LISTEN.')
    return s


def receiver(data, addr):
    """
    Получает принятые данные и анализирует. Если это presence сообщение от залогинившегося пользователя, посылает ему
    приветственное сообщение. Т.к. никакой другой функционал JIM еще не организован, если это не presence,
    вернется ответ о ошибочном действии.
    :param data: JSON, принятый от клиента.
    :param addr: Адрес клиента.
    :return: ответ клиенту в формате string.
    """
    if data.get('action') == 'presence':
        log_message = 'Пришло presence сообщение от клиента ' + addr
        logger.info(log_message)
        log_message = 'Содержимое сообщения: ' + str(data)
        logger.debug(log_message)
        resp = 'You are online!'
    else:
        resp = 'Error action, pal.'
        log_message = 'Пришло что-то неведомое от клиента ' + addr
        logger.info(log_message)
        log_message = 'Содержимое сообщения: ' + str(data)
        logger.debug(log_message)
    return resp


def listen(s):
    """
    Бесконечный цикл, ожидает сообщения от клиента, передает их в декодированном виде в receiver(), для анализа и
    соответствующего действию ответа.
    :param s: сокет, созданный в функции sock_bind
    """
    logger.info('Начинаю ожидать соединения с клиентом.')
    while True:
        client, addr = s.accept()
        data_json = client.recv(1000000)
        if not data_json:
            break
        data = json.loads(data_json.decode('utf-8'))
        print('Пришло сообщение: ', data, ', от клиента: ', addr)
        respond = receiver(data, addr[0])
        client.send(respond.encode('utf-8'))
        client.close()
        log_message = 'Отсоединился клиент ' + addr[0] + '.'
        logger.info(log_message)


# main-функция
def main():
    args = arguments()
    s = sock_bind(args)
    listen(s)


# Точка входа
if __name__ == '__main__':
    main()

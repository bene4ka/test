# Клиентская часть

from socket import *
import sys
import time
import json
import argparse
import logging
import inspect
import names
import client_log_config

logger = logging.getLogger('app.main')


class Log():
    """
    Class of decorator, Used to log functions calls.
    """
    def __init__(self):
        pass

    # Магический метод __call__ позволяет обращаться к
    # объекту класса, как к функции
    def __call__(self, func):
        def decorated(*args, **kwargs):
            def whosdaddy():
                """
                Returns name or the caller funtion.
                :return: caller function name.
                """
                return inspect.stack()[2][3]

            res = func(*args, **kwargs)
            logger.debug(
                'Function {} with args {}, kwargs {} = {} was called '
                'from function {}.'.format(
                    func.__name__, args, kwargs, res, whosdaddy())
            )
            return res

        return decorated


@Log()
def arguments():
    """
    Принимает аргументы командной строки [ip, p, v], где:
    ip - адрес сервера, обязателен к вводу.
    p - порт, к которому будет совершено подключение. По умолчанию равен 7777.
    v - уровень логгирования (0=NOTSET, 1=DEBUG, 2=INFO 3=WARNING 4=ERROR 5=CRITICAL), по-умолчанию 2.
    :return: лист, где первым элементом является порт, а вторым - IP для подключения.
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('ip', metavar='<ip>', help='Server IP address', type=str)
    parser.add_argument('-p', default='7777', help='port of remote server', type=int)
    parser.add_argument('-v', default=2, help='verbose level', type=int)
    parsed_opts = parser.parse_args()
    port = parsed_opts.p
    address = parsed_opts.ip
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
        # Если уровень логгирования выбран неверно, выводим сообщение и глушим клиент.
        logger.setLevel(logging.CRITICAL)
        logger.critical("UNEXPLAINED COUNT IN VERBOSITY LEVEL!")
        print("UNEXPLAINED COUNT IN VERBOSITY LEVEL!")
        sys.exit()
    logger.info('Попытка коннекта будет осуществлена на адрес {} и порт {}'.format(address, str(port)))
    return [port, address]


@Log()
def sock_conn(args):
    """"
    Создает TCP-сокет и подключается к порту и адресу, получеными из функции arguments()
    :param args: лист из порта в integer и адреса сервера в string.
    """
    s = socket(AF_INET, SOCK_STREAM)
    try:
        s.connect((args[1], args[0]))
    except ConnectionRefusedError:
        logger.error('Не удалось соединиться с сервером! Правильный ли ip и порт задан?')
        print('Не удалось соединиться с сервером! Правильный ли ip и порт задан?')
        sys.exit()
    logger.info('Соединение прошло успешно!')
    return s


@Log()
def send_message(s, action_key='presence', type_key='status', user_key='Guest', status_key='I am here!'):
    """
    Создает словарь с ключами action, type, user, затем в формате JSON и кодировке utf-8 отправляет сообщение
    серверу, принимает ответ и выводит его на экран.
    :param s: сокет для соединения
    :param action_key: выполняемое действие, например, presence(статус онлайна) или msg(сообщение).
    :param type_key: тип выполняемого действия
    :param user_key: Имя пользователя
    :param status_key: Статус присутствия
    :return:
    """
    user_key = names.get_full_name()
    logger.info('The name is ' + user_key)
    msg = {
        'action': action_key,
        'time': int(time.time()),
        'type': type_key,
        'user': {
            'user': user_key,
            'status': status_key
        }
    }
    msg_json = json.dumps(msg)
    s.send(msg_json.encode('utf-8'))
    logger.info('Отправлено сообщение серверу.')
    logger.debug('Содержимое сообщения: {}.'.format(msg))
    data = s.recv(1000000)
    logger.info('Получен ответ от сервера.')
    logger.debug('Содержимое ответа: {}.'.format(data.decode('utf-8')))
    print(data.decode('utf-8'))


# main-функция
def main():
    logger.info('Стартован клиент!')
    args = arguments()
    s = sock_conn(args)
    send_message(s, )


# Точка входа
if __name__ == '__main__':
    main()

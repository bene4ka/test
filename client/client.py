# Клиентская часть

from socket import *
import time
import json
import argparse


def arguments():
    """
    Принимает аргументы командной строки [ip, p], где:
    ip - адрес сервера, обязателен к вводу.
    p - порт, к которому будет совершено подключение. По умолчанию равен 7777.
    :return: лист, где первым элементом является порт, а вторым - IP для подключения.
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('ip', metavar='<ip>', help='Server IP address', type=str)
    parser.add_argument('-p',  default='7777', help='port of remote server', type=int)
    parsed_opts = parser.parse_args()
    port = parsed_opts.p
    address = parsed_opts.ip
    return [port, address]


def sock_conn(args):
    """"
    Создает TCP-сокет и подключается к порту и адресу, получеными из функции arguments()
    :param args: лист из порта в integer и адреса сервера в string.
    """
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((args[1], args[0]))
    return s


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
    data = s.recv(1000000)
    print(data.decode('utf-8'))


# main-функция
def main():
    args = arguments()
    s = sock_conn(args)
    send_message(s,)


# Точка входа
if __name__ == '__main__':
    main()

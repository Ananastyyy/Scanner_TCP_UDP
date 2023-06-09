import socket
from threading import Thread

from arguments_parser import get_args
from data import get_db, define_protocol

TCP_ports = []
UDP_ports = []


def scan_ports(target, ports, db):
    sock = None
    for port in ports:
        # определяем тип соединения
        if str(port) in db['tcp']:
            type_connect = 'tcp'
        else:
            type_connect = 'udp'

        # создаем соединение с портом
        try:
            if type_connect == 'tcp':
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(0.5)
            sock.connect((target, port))

        # если не удалось подключиться, значит порт закрыт
        except Exception:
            print(f"{port}/{type_connect} \tclosed")

        else:
            info = f"{port}/{type_connect} \topen "
            message = b'aaa\r\n\r\n'

            # отправляем сообщение на порт
            if type_connect == 'tcp':
                sock.send(message)
            else:
                sock.sendto(message, (target, port))

            protocol = ''
            # получаем ответ
            try:
                data = sock.recv(1028)
                # распознаем протокол из ответа
                protocol = define_protocol(data)
            except socket.timeout:
                pass
            except ConnectionResetError or ConnectionAbortedError:
                pass

            print(info + protocol)
        finally:
            sock.close()


def main():
    args = get_args()

    if args.ports == 'all':
        args.ports = '1-65535'

    ranges = (x.split("-") for x in args.ports.split(","))
    ports = [i for r in ranges for i in range(int(r[0]), int(r[-1]) + 1)]

    db = get_db()

    print(f"Scanning {args.target}...")
    port_offset = len(ports)

    # распараллеливаем работу на 10 потоков
    for i in range(10):
        t = Thread(
            target=scan_ports,
            args=(
                args.target,
                ports[port_offset * i:port_offset * (i + 1)], db,))
        t.start()


if __name__ == '__main__':
    main()

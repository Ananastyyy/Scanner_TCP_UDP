import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'target',
        help='Адрес хоста сканирования')
    parser.add_argument(
        '-p', '--ports',
        default='1-1024',
        help='Список портов для сканирования через ","; также поддерживается ввод диапазона (35,80,5050-6000)')
    return parser.parse_args()

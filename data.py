import csv


# получаем тип соединения у каждого порта
def get_db():
    db = {
        'udp': {},
        'tcp': {}
    }
    with open('port_serv_names.csv') as csv_file:
        data = csv.reader(csv_file)
        for rec in data:
            if rec[0] != 'Service Name':
                try:
                    db[rec[2]].update({rec[1]: rec[0]})
                except KeyError:
                    pass
    return db


# метод определения протокола
def define_protocol(data):
    if b'SMTP' in data:
        return 'SMTP'
    if b'POP3' in data:
        return 'POP3'
    if b'IMAP' in data:
        return 'IMAP'
    if b'HTTP' in data:
        return 'HTTP'
    return ''

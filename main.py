import re
import configparser
import csv
from pprint import pprint


def get_list(file_name):
    with open(file_name, encoding='UTF-8') as file:
        work = csv.reader(file, delimiter=',')
        contacts = list(work)
        return contacts


def get_params(config):
    extract = configparser.ConfigParser()
    extract.read(config)
    select = extract['Telephones']['select']
    order = extract['Telephones']['order']
    return select, order


def change_view(select, order, contacts):
    select = r'{}'.format(select)
    order = r'{}'.format(order)
    changed_list = []
    for person in contacts:
        res = re.sub(select, order, ','.join(person))
        res = re.sub(r'^(\w+).(\w+).(\w+)*', r'\1,\2,\3', res)
        res = re.sub(r',+', r',', res)
        res = re.sub(r' ,', r',', res)
        res = re.sub(r'[\s,]*$', r'', res)
        changed_list.append(res.split(','))
    return changed_list


if __name__ == '__main__':
    change = change_view(*get_params('config.ini'), get_list('phonebook_raw.csv'))
    pprint(change, width=250)
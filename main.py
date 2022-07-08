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
    t_select = extract['Telephones']['select']
    t_order = extract['Telephones']['order']
    n_select = extract['Names']['select']
    n_order = extract['Names']['order']
    return t_select, t_order, n_select, n_order


def change_view(t_select, t_order, n_select, n_order, contacts):
    t_select = r'{}'.format(t_select)
    t_order = r'{}'.format(t_order)
    n_select = r'{}'.format(n_select)
    n_order = r'{}'.format(n_order)
    changed_list = []
    for person in contacts:
        res = re.sub(t_select, t_order, ','.join(person))
        res = re.sub(n_select, n_order, res)
        res = re.sub(r',+', r',', res)
        res = re.sub(r' ,', r',', res)
        res = re.sub(r'[\s,]*$', r'', res)
        res = res.split(',')
        changed_list.append(res)
    return changed_list


if __name__ == '__main__':
    change = change_view(*get_params('config.ini'), get_list('phonebook_raw.csv'))

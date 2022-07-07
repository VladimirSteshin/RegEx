import re
import configparser
import csv
from pprint import pprint


def get_list(file_name):
    with open(file_name, encoding='UTF-8') as file:
        work = csv.reader(file, delimiter=',')
        contacts = list(work)
        return contacts


def get_phone_params(config):
    extract = configparser.ConfigParser()
    extract.read(config)
    select = extract['Telephones']['select']
    order = extract['Telephones']['order']
    return select, order


def change_phone_view(*select_order):
    select, order = select_order
    select = r'{}'.format(select)
    order = r'{}'.format(order)
    print(select)
    print(order)


if __name__ == '__main__':
    get_list('phonebook_raw.csv')
    change_phone_view(*get_phone_params('config.ini'))

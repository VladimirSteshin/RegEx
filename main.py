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
        res = re.sub(r' ,', r',', res)
        res = re.sub(r'(^\w+.\w+.\w+)(,{1,3})', r'\1,', res)
        changed_list.append(res.split(','))
    for person in changed_list:
        if len(person) < len(contacts[0]):
            diff = len(contacts[0]) - len(person)
            for times in range(diff):
                person.insert(3, '')
    return changed_list


def merge(changed_list):
    join = {}
    for person in changed_list:
        key_name = f'{person[0]} {person[1]}'
        info = []
        for data in person[2:]:
            info.append(data)
        if key_name not in join.keys():
            join[key_name] = info
        else:
            for num in range(len(join[key_name])):
                if join[key_name][num] == '' and info[num] != '':
                    join[key_name][num] = info[num]
    return join


if __name__ == '__main__':
    changed = change_view(*get_params('config.ini'), get_list('phonebook_raw.csv'))
    pprint(merge(changed), width=250)

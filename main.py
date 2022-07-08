import re
import csv


def get_list(file_name):
    with open(file_name, encoding='UTF-8') as file:
        work = csv.reader(file, delimiter=',')
        contacts = list(work)
        return contacts


def change_view(select, order, contacts):
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


def get_merge(changed_list):
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
    for value in join.values():
        for num, item in enumerate(value):
            if item == '':
                value[num] = 'No data'
    return join


def get_list_for_write(dict_to_list):
    contacts_list = []
    for key, value in dict_to_list.items():
        get_names = key.split()
        lastname, firstname = get_names[0], get_names[1]
        value.insert(0, firstname)
        value.insert(0, lastname)
        contacts_list.append(value)
    return contacts_list


def write(contacts_list):
    with open("phonebook.csv", "w", encoding='UTF-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


if __name__ == '__main__':
    photos = r'(\+7|8)*[\s\(-]*(\d{3})[\s\)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})[\s\(]*(доб\.)*\s*(\d+)*\)*'
    organise = r'\1(\2)\3-\4-\5 \6\7'
    changed = change_view(photos, organise, get_list('phonebook_raw.csv'))
    merged_dict = get_merge(changed)
    list_for_write = get_list_for_write(merged_dict)
    write(list_for_write)

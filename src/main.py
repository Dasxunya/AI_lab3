import math
import random

import pandas as pd
import numpy as np

data_structure = {}
headlines = []
tree = {}


def main():
    global headlines, data_structure, at, data
    filename = r'C:\Users\Dasxunya\Desktop\ITMO\3\AI\AI_lab3\data\DATA.csv'
    data_csv = pd.read_csv(filename)
    for line in data_csv:
        headlines = line.split(';')[1:]
    print(f'Заголовки: {headlines}')

    # номера позиций атрибутов в структуре (не путать с номером атрибута = название)
    randoms = sorted(random.sample(range(0, 31), int(math.sqrt(145))))
    print(randoms)
    at = list.copy(randoms)

    succes, fail = 0, 0
    for student in data_csv.values:
        s = student[0].split(';')
        data_structure.setdefault(s[0], [])
        for i in range(0, 33):
            data_structure[s[0]] = data_structure[s[0]] + [(headlines[i], s[i + 1])]
            if i == 32:
                if s[i + 1] == 'S':
                    succes += 1
                else:
                    fail += 1
    print(data_structure, '\n', succes, fail)
    data = data_structure
    print(data)

    splitted_d, values = split_by_attribute_values(data_structure, 8)
    print(splitted_d.get('1'))
    info_x_T(splitted_d.get('1'), 8)

    build_tree(data_structure, randoms)
    # позиция атрибута 8 = 9 атрибут


def info_T(s, f):
    global entropy
    summ = s + f
    if s == 0:
        entropy = -((f / summ) * math.log2(f / summ))
    elif f == 0:
        entropy = -((s / summ) * math.log2(s / summ))
    else:
        entropy = -((s / summ) * math.log2(s / summ) + (f / summ) * math.log2(f / summ))
    return entropy


def split_by_attribute_values(d, b_n):
    """Подготовка датасета с учетом значения атрибута"""
    values = {}
    splitted_by_values = {}
    values.setdefault(b_n, [])
    attr_values = prepare_data_b_n(d, b_n)
    values[b_n] = attr_values
    for i in attr_values:
        splitted_by_values.setdefault(i, {})

    for i in attr_values:
        temp = {}
        for j in d:
            if d[j][b_n][1] == i:
                temp.setdefault(j, d[j])
        splitted_by_values[i] = temp

    print(values, splitted_by_values)
    return splitted_by_values, values


def prepare_data_b_n(structure, b_n):
    """Получение информации о значениях в конкретном узле"""
    global info_x
    fields = []
    for j in structure:
        if structure[j][b_n][1] not in fields:
            fields.append(structure[j][b_n][1])
    return fields


def compare_info_x_T(d, attributes):
    """Выбор атрибута с наилучшим информационным приростом"""

    global opt_a
    max_entropy = 0
    counter = 0
    fields_list = [0 for j in range(len(attributes))]
    for i in attributes:
        compare = info_x_T(d, i)
        fields_list[counter] = compare[2]
        counter += 1
        if compare[0] > max_entropy:
            max_entropy = compare[0]
            opt_a = compare[1]

    return opt_a


def info_x_T(splitted_d, attr):
    # splitted_d = {student1: [(attr1, value1), (attr2, value2), ()]), student2: ...}
    global info_x
    fields = {}
    for j in splitted_d:
        if splitted_d[j][attr][1] not in fields:
            fields.setdefault(int(splitted_d[j][attr][1]), [(0, 0, 0)])
    fields_placeholder(attr, fields)
    info_x = 0
    for i in fields:
        info_x = info_x + (fields[i][0][0] / len(splitted_d)) * info_T(fields[i][0][1], fields[i][0][2])
    print(f'для атрибута на позиции {attr} значения {fields} энтропия =', info_x)
    return info_x, attr, fields


def fields_placeholder(a, f):
    """Подсчет количества успехов и неудач среди значения атрибута"""
    for i in f:
        k, k_s, k_f = 0, 0, 0
        for r in data_structure:
            if int(data_structure[r][a][1]) == i and data_structure[r][32][1] == 'S':
                k = k + 1
                k_s = k_s + 1
                f[i][0] = (k, k_s, k_f)
            if int(data_structure[r][a][1]) == i and data_structure[r][32][1] == 'F':
                k = k + 1
                k_f = k_f + 1
                f[i][0] = (k, k_s, k_f)
    return f


def build_tree(d, attrs, node=None, order=0):
    # {узел1: {ребро1: дочерний_узел1, ребро2: дочерний_узел2}, узел2:...}
    # while node != 'S' or node != 'F':
        if order == 0:
            best_node = compare_info_x_T(d, attrs)  # получили оптимальную вершину
            s_b_v, v = split_by_attribute_values(d, best_node)  # получили информацию о значениях вершины и разбили мн-во на подм-ва(s_b_v)
            print(v[best_node], '\n', best_node)
            for i in v[best_node]:
                print(i)
        # else:
        #


main()

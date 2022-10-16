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

    node = compare_gain(data_structure, randoms)
    randoms.remove(node)
    build_tree(data_structure, randoms, node)
    # позиция атрибута 8 = 9 атрибут


def info_T(s, f):
    global entropy
    summ = s + f
    if s == 0:
        entropy = -((f / math.fabs(summ)) * math.log2(f / math.fabs(summ)))
    elif f == 0:
        entropy = -((s / math.fabs(summ)) * math.log2(s / math.fabs(summ)))
    else:
        entropy = -((s / math.fabs(summ)) * math.log2(s / math.fabs(summ)) + (f / math.fabs(summ)) * math.log2(
            f / math.fabs(summ)))
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

    print(values)
    return splitted_by_values, values


def prepare_data_b_n(structure, b_n):
    """Получение информации о значениях в конкретном узле"""
    global info_x
    fields = []
    for j in structure:
        if structure[j][b_n][1] not in fields:
            fields.append(structure[j][b_n][1])
    return fields


def compare_gain(d, attributes):
    """Выбор атрибута с наилучшим информационным приростом"""
    global opt_a, max_g
    max_entropy = 0
    counter = 0
    fields_list = [0 for j in range(len(attributes))]
    for i in attributes:
        compare = info_x_T(d, i)
        fields_list[counter] = compare[2]
        counter += 1
    attr_to_values = dict(zip(attributes, fields_list))
    print(attr_to_values, '\n', fields_list)

    succes = 0
    fail = 0
    for i in d:
        s = d.get(i)
        for j in range(0, 33):
            if j == 32:
                if s[j][1] == 'S':
                    succes += 1
                else:
                    fail += 1

    print(succes, fail)
    max_g = 0
    for i in attributes:
        infos = info_x_T(d, i)[0]
        splits = split_info_x(d, i, attr_to_values)
        gain = (info_T(succes, fail) - infos) / splits
        if gain > max_g:
            max_g = gain
            opt_a = i
            print(infos, splits, gain)
    return opt_a


def info_x_T(splitted_d, attr):
    # splitted_d = {student1: [(attr1, value1), (attr2, value2), ()]), student2: ...}
    global info_x
    fields = {}
    for j in splitted_d:
        if splitted_d[j][attr][1] not in fields:
            fields.setdefault(int(splitted_d[j][attr][1]), [(0, 0, 0)])
    fields_placeholder(splitted_d, attr, fields)
    info_x = 0
    for i in fields:
        info_x = info_x + (math.fabs(fields[i][0][0]) / math.fabs(len(splitted_d))) * info_T(fields[i][0][1],
                                                                                             fields[i][0][2])
    print(f'для атрибута на позиции {attr} значения {fields} энтропия =', info_x)
    return info_x, attr, fields


def split_info_x(d, attr, attr_to_values):
    split = 0
    for i in attr_to_values[attr]:
        var = math.fabs(attr_to_values[attr][i][0][0]) / math.fabs(len(d))
        split = split - (var * math.log2(var))
    print(split)
    return split


def fields_placeholder(s_d, a, f):
    """Подсчет количества успехов и неудач среди значения атрибута"""
    for i in f:
        k, k_s, k_f = 0, 0, 0
        for r in s_d:
            if int(s_d[r][a][1]) == i and data_structure[r][32][1] == 'S':
                k = k + 1
                k_s = k_s + 1
                f[i][0] = (k, k_s, k_f)
            if int(s_d[r][a][1]) == i and s_d[r][32][1] == 'F':
                k = k + 1
                k_f = k_f + 1
                f[i][0] = (k, k_s, k_f)
    return f


def build_tree(d, attrs, node, order=0):
    #
    global best_node
    print(attrs)
    best_node = node
    s_b_v, v = split_by_attribute_values(d, best_node)
    print(v, best_node)
    local_attrs = attrs

    if len(local_attrs) == 1:
        return

    for i in v[best_node]:
        print(best_node, 'level =', order + 1)
        best_node = compare_gain(d, local_attrs)
        build_tree(s_b_v[i], local_attrs, best_node, order + 1)


main()

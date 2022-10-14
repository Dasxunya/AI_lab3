import math
import random

import pandas as pd
import numpy as np

data_structure = {}
headlines = []
tree = {}


def main():
    global headlines, data_structure
    filename = r'C:\Users\Dasxunya\Desktop\ITMO\3\AI\AI_lab3\data\DATA.csv'
    data_csv = pd.read_csv(filename)
    for line in data_csv:
        headlines = line.split(';')[1:]
    print(f'Заголовки: {headlines}')

    # номера позиций атрибутов в структуре (не путать с номером атрибута = название)
    randoms = sorted(random.sample(range(0, 31), int(math.sqrt(145))))
    print(randoms)

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
    entropy = info_T(succes, fail)
    compare_info_x_T(randoms)


def info_T(s, f):
    sum = s + f
    entropy = -((s / sum) * math.log2(s / sum) + (f / sum) * math.log2(f / sum))
    return entropy


def compare_info_x_T(attributes):
    for i in attributes:
        info_x_T(i)


def info_x_T(attribute):
    # {характеристика1: [(count, success-count, fails-count)], характеристика2: [(count, success-count, fails-count),...}
    fields = {}
    print(attribute + 1)
    for j in data_structure:
        if data_structure[j][attribute][1] not in fields:
            fields.setdefault(int(data_structure[j][attribute][1]), [(0, 0, 0)])

    fields_placeholder(attribute, fields)


def fields_placeholder(a, f):
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
    print(f)


main()

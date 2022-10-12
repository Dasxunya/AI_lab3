import math
import random

import pandas as pd
import numpy as np

data_structure = {}
headlines = []
attributes = []


def main():
    global headlines, data_structure
    filename = r'C:\Users\Dasxunya\Desktop\ITMO\3\AI\AI_lab3\data\DATA.csv'
    data_csv = pd.read_csv(filename)
    for line in data_csv:
        headlines = line.split(';')[1:]
    print(f'Заголовки: {headlines}')

    randoms = random.sample(range(1, 34), int(math.sqrt(145)))
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


def info_T(s, f):
    sum = s + f
    entropy = -((s / sum) * math.log2(s / sum) + (f / sum) * math.log2(f / sum))
    return entropy


def info_x_T(attributes):
    i = 0


# def file_input(filename):
#     with open(filename, 'r', encoding='utf-8') as file:
#         for line in file:


main()

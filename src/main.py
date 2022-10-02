import pandas as pd
import numpy as np

data_structure = {}
headlines = []


def main():
    global headlines, data_structure
    filename = r'C:\Users\Dasxunya\Desktop\ITMO\3\AI\AI_lab3\data\DATA.csv'
    data_csv = pd.read_csv(filename)
    for line in data_csv:
        headlines = line.split(';')[1:]
    print(f'Заголовки: {headlines}')
    for student in data_csv.values:
        s = student[0].split(';')
        data_structure.setdefault(s[0], [])
        for i in range(0, 33):
            data_structure[s[0]] = data_structure[s[0]] + [(headlines[i], s[i+1])]

    print(data_structure)


# def file_input(filename):
#     with open(filename, 'r', encoding='utf-8') as file:
#         for line in file:


main()

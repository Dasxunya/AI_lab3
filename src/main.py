import json
import math
import random
import pandas as pd

result = 'PROGRESS'
headlines = []
tree = {'a_name': '', 'a_value': '', 'result': '', 'edges': []}


def main():
    global headlines
    filename = r'C:\Users\Dasxunya\Desktop\ITMO\3\AI\AI_lab3\data\DATA.csv'
    tree_name = r'C:\Users\Dasxunya\Desktop\ITMO\3\AI\AI_lab3\data\tree.json'
    table = pd.read_csv(filename, delimiter=";", index_col="STUDENT ID")

    randoms = sorted(random.sample(range(1, 32), int(math.sqrt(32))))
    for i in table.columns:
        if i == 'PROGRESS':
            continue
        if i == 'GRADE':
            del table['GRADE']
        elif int(i) not in randoms:
            del table[i]
    print(table)
    res = build_tree(table, result, tree)
    tree_json = json.dumps(res, indent=4, sort_keys=True)
    with open(tree_name, 'w') as file:
        file.write(tree_json)


def info_T(splitted_data):
    """Оценка среднего количества информации, необходимого для определения класса примера из
множества T (энтропия):"""
    global entropy
    count = splitted_data['PROGRESS'].value_counts()
    s = count.get('S')
    f = count.get('F')
    summ = s + f
    if s == 0:
        entropy = -((f / math.fabs(summ)) * math.log2(f / math.fabs(summ)))
    elif f == 0:
        entropy = -((s / math.fabs(summ)) * math.log2(s / math.fabs(summ)))
    else:
        entropy = -((s / math.fabs(summ)) * math.log2(s / math.fabs(summ)) + (f / math.fabs(summ)) * math.log2(
            f / math.fabs(summ)))
    print('entropy:', entropy)
    return entropy


def info_x_T(splitted_data, attr):
    """Оценка среднего количества информации, необходимого для определения класса примера из
множества после разбиения множества по (условная энтропия)"""
    conditional_entropy = 0
    values = splitted_data[attr].value_counts()

    for i in values.index:
        conditional_entropy = conditional_entropy + (math.fabs(values.get(i)) / math.fabs(len(splitted_data))) * info_T(
            splitted_data)
    print('условная энтропия:', conditional_entropy)
    return conditional_entropy


def split_info_x(splitted_data, attr):
    """Оценка потенциальной информации, получаемой при разбиении множества на подмножеств.
Необходим для учета атрибутов с уникальными значениями"""
    split = 0
    values = splitted_data[attr].value_counts()
    print(values)
    for i in values.index:
        split -= (math.fabs(values.get(i)) / math.fabs(len(splitted_data))) * math.log2(
            math.fabs(values.get(i)) / math.fabs(len(splitted_data)))
    print('split:', split)
    return split


def gain_ratio_x(splitted_data, attr):
    """Нормированный прирост"""
    diff = (info_T(splitted_data) - info_x_T(splitted_data, attr))
    split = split_info_x(splitted_data, attr)
    if split != 0:
        gain = diff / split
    else:
        gain = 0
    print('gain:', gain)
    return gain


def frequency(splitted_data, value):
    """Количество значения атрибута в колонке класса"""
    g = splitted_data[result].value_counts()
    count = g.get(value)
    return count


def build_tree(splitted_data, attr, parent_tree):
    """Построение дерева решений"""
    max_gain = 0
    root = ''
    for i in splitted_data.columns:
        if i != attr and i != 'GRADE':
            gain = gain_ratio_x(splitted_data, i)
            if gain >= max_gain:
                max_gain = gain
                root = i

    if root == '':
        return

    grouped = splitted_data.groupby(root)
    for subtable, subtable_df in grouped:
        v = subtable_df[root].iloc[0]
        if len(subtable_df.columns) == 2 and len(subtable_df[attr].unique()) != 1:
            child_tree = {'edges': [], 'a_name': int(root), 'a_value': int(v),
                          'result': 'S' if frequency(splitted_data, 'S') >= frequency(splitted_data, 'F') else 'F'}

            parent_tree['edges'].append(child_tree)
        elif len(subtable_df[attr].unique()) == 1:
            child_tree = {'edges': [], 'a_name': int(root), 'a_value': int(v), 'result': subtable_df[attr].iloc[0]}
            parent_tree['edges'].append(child_tree)
        else:
            del subtable_df[root]
            child_tree = {'edges': [], 'a_name': int(root), 'a_value': int(v), 'result': ''}
            parent_tree['edges'].append(build_tree(subtable_df, attr, child_tree))
    return parent_tree


main()

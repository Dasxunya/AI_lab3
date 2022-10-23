import json
import math
import random
import pandas as pd
from MultiColumnLabelEncoder import MultiColumnLabelEncoder
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import roc_curve, auc, precision_recall_curve

result = 'PROGRESS'
tree = {'a_name': '', 'a_value': '', 'result': '', 'edges': []}


def main():
    global headlines
    filename = r'C:\Users\Dasxunya\Desktop\ITMO\3\AI\AI_lab3\data\DATA.csv'
    tree_name = r'C:\Users\Dasxunya\Desktop\ITMO\3\AI\AI_lab3\data\tree.json'
    table = pd.read_csv(filename, delimiter=";", index_col="STUDENT ID")

    X = table['PROGRESS']
    y = table.drop('PROGRESS', axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8)
    table = pd.concat([y_train, X_train], sort=False, axis=1)
    tests = y_test

    randoms = sorted(random.sample(range(1, 32), int(math.sqrt(32))))
    for i in table.columns:
        if i == 'PROGRESS':
            continue
        if i == 'GRADE':
            del table['GRADE']
            del y_test['GRADE']
        elif int(i) not in randoms:
            del table[i]
            del y_test[i]

    res = build_tree(table, result, tree)

    tree_json = json.dumps(res, indent=4, sort_keys=True)

    with open(tree_name, 'w') as file:
        file.write(tree_json)

    res_test = []
    for i in range(len(y_test)):
        row_res = set_class(res['edges'], y_test.iloc[i, :])
        res_test.append(row_res)
    y_test['PROGRESS'] = res_test

    tp, fp, fn, tn = compare_class(X_test, y_test)
    acc = accuracy(tp, fp, fn, tn)
    prec = precision(tp, fp)
    rec = recall(tp, fn)
    print(f'Accuracy: {acc}\nPrecision: {prec}\nRecall: {rec}')

    # вместо 'S' и 'F' 1 и 0 соответственно, лист значений классов - test_x
    test_x = X_test
    for i in range(len(res_test)):
        if res_test[i] == 'S':
            test_x[i] = 1
        else:
            test_x[i] = 0
    # лист данных построчно без result
    del tests[result]
    #
    # ---------------------------------------------------
    #
    # отрисовка графика
    data = pd.read_csv(filename, delimiter=";", index_col="STUDENT ID")
    y = data[result]
    data = data.drop(result, axis=1)
    X = data.sample(n=6, axis='columns')
    clf = SVC()
    my_y = y.copy().to_numpy()
    my_y[my_y == 'S'] = 1
    my_y[my_y == 'F'] = 0
    my_y = my_y.astype('int')

    my_X = X.copy()
    my_X = MultiColumnLabelEncoder().fit_transform(my_X)
    my_X = my_X.to_numpy()

    limit = int(len(data) * 0.8)
    my_training_X = my_X[:limit, :]
    my_test_X = my_X[limit:, :]

    my_training_y = my_y[:limit]
    y_true_list = my_y[limit:]

    y_score = clf.fit(my_training_X, my_training_y)
    y_score = clf.decision_function(my_test_X)
    # AUC ROC
    fpr, tpr, treshold = roc_curve(y_true_list, y_score)
    plt.plot(fpr, tpr)
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()
    #AUC PR
    p, r, thresholds = precision_recall_curve(y_true_list, y_score)
    plt.plot(r, p)
    plt.ylabel('Precision')
    plt.xlabel('Recall/True positive Rate')
    plt.show()


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
    return entropy


def info_x_T(splitted_data, attr):
    """Оценка среднего количества информации, необходимого для определения класса примера из
множества после разбиения множества по (условная энтропия)"""
    conditional_entropy = 0
    values = splitted_data[attr].value_counts()

    for i in values.index:
        conditional_entropy = conditional_entropy + (math.fabs(values.get(i)) / math.fabs(len(splitted_data))) * info_T(
            splitted_data)
    return conditional_entropy


def split_info_x(splitted_data, attr):
    """Оценка потенциальной информации, получаемой при разбиении множества на подмножеств.
Необходим для учета атрибутов с уникальными значениями"""
    split = 0
    values = splitted_data[attr].value_counts()
    for i in values.index:
        split -= (math.fabs(values.get(i)) / math.fabs(len(splitted_data))) * math.log2(
            math.fabs(values.get(i)) / math.fabs(len(splitted_data)))
    return split


def gain_ratio_x(splitted_data, attr):
    """Нормированный прирост"""
    diff = (info_T(splitted_data) - info_x_T(splitted_data, attr))
    split = split_info_x(splitted_data, attr)
    if split != 0:
        gain = diff / split
    else:
        gain = 0
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
        if i != attr:
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
                          'result': 'S' if frequency(splitted_data, 'S') > frequency(splitted_data, 'F') else 'F'}
            parent_tree['edges'].append(child_tree)
        elif len(subtable_df[attr].unique()) == 1:
            child_tree = {'edges': [], 'a_name': int(root), 'a_value': int(v), 'result': subtable_df[attr].iloc[0]}
            parent_tree['edges'].append(child_tree)
        else:
            del subtable_df[root]
            child_tree = {'edges': [], 'a_name': int(root), 'a_value': int(v), 'result': ''}
            parent_tree['edges'].append(build_tree(subtable_df, attr, child_tree))
            if None in child_tree['edges']:
                for i in child_tree['edges']:
                    if i is None:
                        child_tree['edges'].remove(i)
    return parent_tree


def set_class(t, row):
    """Установить класс тестовому набору по обучающим данным"""
    for node in t:
        if row[str(node['a_name'])] == node['a_value']:
            if node['result'] != '':
                b = node['result']
                return b
            else:
                return set_class(node['edges'], row)
        else:
            continue


def compare_class(wait, real):
    tp, fp, fn, tn = 0, 0, 0, 0
    for i in real.index:
        if real[result][i] == 'S':
            if wait[i] == 'S':
                tp += 1
            else:
                fp += 1
        else:
            if wait[i] == 'F':
                tn += 1
            else:
                fn += 1
    return tp, fp, fn, tn


def accuracy(tp, fp, fn, tn):
    if (tp + fp + fn + tn) == 0:
        return 0
    return (tp + tn) / (tp + fp + fn + tn)


def precision(tp, fp):
    if (tp + fp) == 0:
        return 0
    return tp / (tp + fp)


def recall(tp, fn):
    if (tp, fn) == 0:
        return 0
    return tp / (tp + fn)


main()

import numpy as np
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
import random
import time


def edit_distance(x, y):
    a = len(x)
    b = len(y)
    edit_table = np.zeros((a+1, b+1))
    for i in range(a + 1):
        edit_table[i, 0] = i
    for j in range(b + 1):
        edit_table[0, j] = j
    for i in range(a):
        k = i + 1
        for j in range(b):
            l = j + 1
            if x[k-1] == y[l-1]:
                edit_table[k][l] = edit_table[k-1][l-1]
            else:
                edit_table[k][l] = 1 + min(min(edit_table[k][l - 1], edit_table[k - 1][l - 1]), edit_table[k - 1][l])
    return edit_table[a][b], edit_table


def create_sequence(x, y):
    rebuild = []
    a, b = len(x), len(y)

    dist, dist_table = edit_distance(x, y)
    print("Odległość edycyjna: " + str(dist))

    while a != 0 or b != 0:
        min_i, min_j = a - 1, b - 1
        if dist_table[min_i][min_j] > dist_table[a - 1][b]:
            min_i, min_j = a - 1, b
        if dist_table[min_i][min_j] > dist_table[a][b - 1]:
            min_i, min_j = a, b - 1

        if min_i == a - 1 and min_j == b - 1:
            # zamiana liter
            if dist_table[min_i][min_j] != dist_table[a][b]:
                rebuild.append((1, a, b))
            a, b = a - 1, b - 1
        elif min_i == a - 1 and min_j == b:
            # usunięcie litery
            rebuild.append((2, a, b))
            a -= 1
        else:
            # dodanie litery
            rebuild.append((3, a, b))
            b -= 1
    return rebuild


def rebuild_x_to_y(x, y):
    rebuild = create_sequence(x, y)
    a, b = len(x), len(y)
    transform_x_to_y = list(x)
    print("".join(transform_x_to_y))
    for (i, j, k) in rebuild:
        if i == 1:
            transform_x_to_y[j - 1] = y[k - 1]
            if j == a:
                print("".join(transform_x_to_y[:j-1]) + "*" + y[k-1] + "*", "zamiana")
            elif j == 1:
                print("*" + y[k - 1] + "*" + "".join(transform_x_to_y[j:]), "zamiana")
            else:
                print("".join(transform_x_to_y[:j - 1]) + "*" + y[k - 1] + "*" + "".join(transform_x_to_y[j:]), "zamiana")
        elif i == 2:
            if j == a:
                print("".join(transform_x_to_y[:j-1]) + "*", "usunięcie")
            elif j == 1:
                print("*" + "".join(transform_x_to_y[j:]), "usunięcie")
            else:
                print("".join(transform_x_to_y[:j-1]) + "*" + "".join(transform_x_to_y[j:]), "usunięcie")
            del transform_x_to_y[j - 1]
        else:
            if j == a:
                print("".join(transform_x_to_y[:j-1]) + "*" + y[k - 1] + "*", "dodanie")
            elif j == 0:
                print("*" + y[k - 1] + "*" + "".join(transform_x_to_y[j:]), "dodanie")
            else:
                print("".join(transform_x_to_y[:j]) + "*" + y[k - 1] + "*" + "".join(transform_x_to_y[j:]), "dodanie")
            transform_x_to_y.insert(j, y[k - 1])

    print("".join(transform_x_to_y))


rebuild_x_to_y("los", "kloc")
print(30 * "-")
rebuild_x_to_y("Łódź", "Lodz")
print(30 * "-")
rebuild_x_to_y("kwintesencja", "quintessence")
print(30 * "-")
rebuild_x_to_y("ATGAATCTTACCGCCTCG", "ATGAGGCTCTGGCCCCTG")
print(30 * "-")


def lcs(x, y):
    a = len(x)
    b = len(y)
    res = np.zeros((a+1, b+1))
    for i in range(a+1):
        res[i, 0] = 0
    for j in range(b+1):
        res[0, j] = 0
    for i in range(a+1):
        for j in range(b+1):
            if x[i - 1] == y[j - 1]:
                res[i, j] = res[i-1, j-1] + 1
            else:
                res[i,j] = max(res[i, j-1], res[i-1, j])
    return res[a, b], res


print("los i kloc ", lcs("los","kloc")[0])
print("łódź i lodz ", lcs("Łódź","Lodz")[0])
print("kwintesencja i quintessence ", lcs("kwintesencja","quintessence")[0])
print("ATGAATCTTACCGCCTCG i ATGAGGCTCTGGCCCCTG", lcs("ATGAATCTTACCGCCTCG","ATGAGGCTCTGGCCCCTG")[0])
print(30 * "*")


def remove_random_tokens(tokens, percentage):
    to_delete = [random.choice(tokens) for _ in range(int(len(tokens)*percentage/100))]
    return [token for token in tokens if token not in to_delete]


def custom_diff(x, y, tokens):
    diff = []
    _, lcs_arr = lcs(x, y)
    a = len(x)
    b = len(y)
    while a != 0 or b != 0:
        if x[a - 1] == y[b - 1]:
            diff.append(x[a - 1])
            a, b = a - 1, b - 1
        elif lcs_arr[a - 1][b] > lcs_arr[a][b - 1]:
            a -= 1
        else:
            b -= 1
    diff.reverse()
    i, j = 0, 0
    output = [token for token in tokens if token not in diff]
    print("Tokey nie należące do LCS: " + str(output))
    for line in diff:
        while (i < len(x) and x[i] != line) or (j < len(y) and y[j] != line):
            if i < len(x) and x[i] != line:
                print("< " + str(i + 1), x[i])
                i += 1
            if j < len(y) and y[j] != line:
                print("> " + str(j + 1), y[i])
                j += 1


with open("romeo-i-julia-700.txt", 'r', encoding="utf-8") as f:
    content = f.read()
    nlp = English()
    tokenizer = nlp.Defaults.create_tokenizer(nlp)

    tokens = [token for token in tokenizer(content) if not token.is_space]
    print("Tokeny: " + str(len(tokens)))

    cut_content1 = remove_random_tokens(tokens, 3)
    cut_content2 = remove_random_tokens(tokens, 3)

    tokens_lcs = lcs(cut_content1,cut_content2)[0]
    print("Długość LCS dla dwóch wyciętych zawartości: " + str(tokens_lcs))
    
    custom_diff(cut_content1, cut_content2, tokens)




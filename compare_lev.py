import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="input filename")
parser.add_argument("--output", help="output filename")
args = parser.parse_args()

with open(args.input) as f:
    names_of_compare = f.read().split('\n')

def levenshtein_distance(line_1, line_2):
    size_x = len(line_1) + 1
    size_y = len(line_2) + 1
    matrix = [[0] * (size_y) for row in range(size_x)]
    
    for x in range(size_x):
        matrix[x][0] = x
    for y in range(size_y):
        matrix[0][y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if line_1[x - 1] == line_2[y - 1]:
                matrix[x][y] = min(
                    matrix[x - 1][y] + 1,
                    matrix[x - 1][y - 1],
                    matrix[x][y - 1] + 1
                )
            else:
                matrix[x][y] = min(
                    matrix[x - 1][y] + 1,
                    matrix[x - 1][y - 1] + 1,
                    matrix[x][y - 1] + 1
                )
    return (matrix[size_x - 1][size_y - 1])

final_metrics = []

for i in range(len(names_of_compare)):
    file_1, file_2 = names_of_compare[i].split()

    with open(file_1, encoding='utf-8') as f:
        token_1 = f.read().lower().replace('\n', ' ')

    with open(file_2, encoding='utf-8') as r:
        token_2 = r.read().lower().replace('\n', ' ')

    token_1 = re.sub(r"\[.*\]|\{.*\}", "", token_1)
    token_1 = re.sub(r'[^\w\s]', "", token_1)

    token_2 = re.sub(r"\[.*\]|\{.*\}", "", token_2)
    token_2 = re.sub(r'[^\w\s]', "", token_2)

    final_metric = levenshtein_distance(token_1.split(), token_2.split()) / max(len(token_1.split()), len(token_1.split()))
    final_metrics.append(final_metric)

with open(args.output, 'w') as fp:
    for item in final_metrics:
        fp.write("{}\n".format(item))

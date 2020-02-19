import os
from collections import Counter
import numpy as np
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))

file_names = ['a_example', 'b_small', 'c_medium', 'd_quite_big', 'e_also_big']
input_files = [os.path.join(dir_path, 'input', '{}.in'.format(file_name)) for file_name in file_names]
output_files = [os.path.join(dir_path, 'output', '{}.out'.format(file_name)) for file_name in file_names]


def compute_score():
    # kadeco
    s = pd.Series([1, 3, 5, np.nan, 6, 8])
    print(s)
    print(Counter('abracadabra').most_common(3))


def process(input_file_path, output_file_path):
    output_file = open(output_file_path, 'w')

    with open(input_file_path) as input_file:
        for line in input_file:
            output_file.write(line)


def main():
    for index, input_file_path in enumerate(input_files):
        process(input_file_path, output_files[index])
    compute_score()


if __name__ == "__main__":
    main()

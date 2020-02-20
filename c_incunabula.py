import os
import time
from collections import Counter, OrderedDict
from copy import deepcopy

import numpy as np
import pandas as pd
from tqdm import tqdm

dir_path = os.path.dirname(os.path.realpath(__file__))

file_names = ['f_libraries_of_the_world']
input_files = [os.path.join(dir_path, 'input', '{}.txt'.format(file_name)) for file_name in file_names]
output_files = [os.path.join(dir_path, 'output', '{}.out'.format(file_name)) for file_name in file_names]


def process(input_file_path, output_file_path):
    output_file = open(output_file_path, 'w')
    number_of_books = None
    number_of_libraries = None
    len_days = None
    books_scores = []
    library_definition = {
    }
    library_sign_len = {}
    library_books = {
    }

    result_libraries = OrderedDict()

    with open(input_file_path) as input_file:
        lib_index = 0
        for index, line in enumerate(input_file.readlines()):
            line_striped = line.strip()
            if len(line_striped) == 0:
                continue
            if index == 0:
                number_of_books, number_of_libraries, len_days = [int(i) for i in line_striped.split(' ')]
            elif index == 1:
                books_scores = [int(i) for i in line.split(' ')]
            elif index % 2 == 0:
                # lib definition
                definition = [int(i) for i in line_striped.split(' ')]
                library_definition[lib_index] = definition
                library_sign_len[lib_index] = definition[1]
            else:
                # books in lib
                library_books[lib_index] = set([int(i) for i in line_striped.split(' ')])
                lib_index += 1

    # lib with score defined as score/pocet dni na sign up
    library_books_2 = deepcopy(library_books)
    good_libraries = []

    # for lib, book in library_books_2.items():
    def _compute_score():
        lib_by_score = {}
        for lib, lib_books in library_books.items():
            lib_books_score = sum([books_scores[i] for i in lib_books])
            lib_by_score[lib] = lib_books_score / library_sign_len[lib]
        lib_by_score = {k: v for k, v in sorted(lib_by_score.items(), key=lambda item: item[1], reverse=True)}

        best_lib = next(iter(lib_by_score))
        books_to_remove = library_books[best_lib]
        good_libraries.append(best_lib)
        if len(books_to_remove) != 0:
            result_libraries[best_lib] = books_to_remove
            del library_books[best_lib]
            for lib, books in library_books.items():
                library_books[lib] = books - books_to_remove

    start_time = time.time()
    while len(good_libraries) != number_of_libraries:
        _compute_score()
    print("--- %s seconds ---" % (time.time() - start_time))

    output_file.write('{}\n'.format(len(result_libraries.keys())))
    for result_lib, result_books in result_libraries.items():
        output_file.write('{} {}\n'.format(result_lib, len(result_books)))
        output_file.write('{}\n'.format(' '.join([str(book) for book in result_books])))
    output_file.close()

    # compute score
    # print(books)
    # result_score = 0
    #
    # for day in enumerate(1, len_days + 1):
    #     lib, books = result_libraries.popitem(last=False)
    #     sign_up_len = library_definition[lib][1]
    #
    # for result_lib, result_books in result_libraries.items():
    #     len_days -= library_definition[result_lib][1]
    #     if len_days == 0:
    #         break
    #     for book in result_books:
    #         result_score += books[book]
    #         books[book] = 0
    # print(result_score)
    # compute score


def main():
    for index, input_file_path in enumerate(input_files):
        process(input_file_path, output_files[index])


if __name__ == "__main__":
    main()

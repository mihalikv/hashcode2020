import os
from collections import Counter, OrderedDict
import numpy as np
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))

file_names = ['d_tough_choices']
input_files = [os.path.join(dir_path, 'input', '{}.txt'.format(file_name)) for file_name in file_names]
output_files = [os.path.join(dir_path, 'output', '{}.out'.format(file_name)) for file_name in file_names]


def process(input_file_path, output_file_path):
    output_file = open(output_file_path, 'w')
    number_of_books = None
    number_of_libraries = None
    len_days = None
    books_scores = []
    books_scores_dict = OrderedDict({})
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
                books_scores_dict = {k: v for k, v in enumerate(books_scores)}
            elif index % 2 == 0:
                # lib definition
                definition = [int(i) for i in line_striped.split(' ')]
                library_definition[lib_index] = definition
                library_sign_len[lib_index] = definition[1]
            else:
                # books in lib
                library_books[lib_index] = [int(i) for i in line_striped.split(' ')]
                lib_index += 1

    # sort books by score
    # for lib, books in library_books.items():
    #     books.sort(key=lambda book_index: books_scores[book_index], reverse=True)
    # sort books by score

    days_left = len_days

    def _get_score():
        best_lib = None
        best_lib_score = None
        best_lib_books = None
        for lib, definition in library_definition.items():
            days_available = (days_left - definition[1]) * definition[2]
            sum_lib_per_days = sum([books_scores[i] for i in library_books[lib][:days_available]]) / definition[1]
            if best_lib_score is None or best_lib_score < sum_lib_per_days:
                best_lib_score = sum_lib_per_days
                best_lib = lib
                best_lib_books = library_books[lib][:days_available]
        return best_lib, best_lib_books

    while days_left > -100:
        good_library, good_books = _get_score()
        days_left -= library_definition[good_library][1]
        del library_definition[good_library]
        result_libraries[good_library] = good_books
        print(days_left)
        for lib, books in library_books.items():
            library_books[lib] = list(set(books)-set(good_books))
            library_books[lib].sort(key=lambda book_index: books_scores[book_index], reverse=True)

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

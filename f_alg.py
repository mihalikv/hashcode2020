import os
from collections import OrderedDict
from copy import deepcopy

dir_path = os.path.dirname(os.path.realpath(__file__))

file_names = ['e_so_many_books']
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
    num_books_in_libs = {}
    for lib, books in library_books.items():
        for book in books:
            if book in num_books_in_libs:
                num_books_in_libs[book] += 1
            else:
                num_books_in_libs[book] = 1
    for book, occurrence in num_books_in_libs.items():
        num_books_in_libs[book] = 1/occurrence
    score_of_book_by_unique = OrderedDict(sorted(num_books_in_libs.items(), key=lambda x: x[1], reverse=True))



    library_definition_orig = deepcopy(library_definition)
    days_left = len_days

    def _get_score():
        best_lib = None
        best_lib_score = None
        best_lib_books = None
        for lib, definition in library_definition.items():
            days_available = (days_left - definition[1]) * definition[2]
            used_books = library_books[lib][:days_available]
            if len(used_books) == 0:
                continue
            score_by_uniqnes = sum([score_of_book_by_unique[book] for book in used_books]) / len(used_books)  # 1 best or 0.0001 worst
            sum_lib_per_days = (sum([books_scores[i] for i in used_books]) / definition[1]) * score_by_uniqnes
            if best_lib_score is None or best_lib_score < sum_lib_per_days:
                best_lib_score = sum_lib_per_days
                best_lib = lib
                best_lib_books = library_books[lib][:days_available]
        return best_lib, best_lib_books

    while days_left > -100:
        good_library, good_books = _get_score()
        if good_library is None:
            break

        days_left_test = days_left - library_definition[good_library][1]
        del library_definition[good_library]
        if days_left_test < 0:
            continue
        days_left = days_left_test
        if len(good_books) > 0:
            result_libraries[good_library] = good_books
        print(days_left)
        for lib, books in library_books.items():
            library_books[lib] = list(set(books) - set(good_books))
            library_books[lib].sort(key=lambda book_index: books_scores[book_index], reverse=True)

    output_file.write('{}\n'.format(len(result_libraries.keys())))
    for result_lib, result_books in result_libraries.items():
        output_file.write('{} {}\n'.format(result_lib, len(result_books)))
        output_file.write('{}\n'.format(' '.join([str(book) for book in result_books])))
    output_file.close()

    # compute score
    result_score = 0
    already_scanned = []
    current_in_scan = OrderedDict()

    for day in range(0, len_days):
        lib_to_remove = []
        for lib in current_in_scan.keys():
            for i in range(library_definition_orig[lib][2]):
                book_index = current_in_scan[lib].pop(0)
                if book_index not in already_scanned:
                    result_score += books_scores_dict[book_index]
                if len(current_in_scan[lib]) == 0:
                    lib_to_remove.append(lib)
                    break
        for lib in lib_to_remove:
            del current_in_scan[lib]
        libs = list(result_libraries.keys())
        if len(libs) == 0:
            continue
        selected_lib = libs[0]
        library_definition_orig[selected_lib][1] = library_definition_orig[selected_lib][1] - 1
        sign_up_len = library_definition_orig[selected_lib][1]
        if sign_up_len == 0:
            current_in_scan[selected_lib] = result_libraries[selected_lib]
            del result_libraries[selected_lib]

    print('score: {}'.format(result_score))
    # compute score


def main():
    for index, input_file_path in enumerate(input_files):
        process(input_file_path, output_files[index])


if __name__ == "__main__":
    main()

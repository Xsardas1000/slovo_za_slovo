import numpy as np
import re, os, time
from collections import defaultdict
import textwrap
ROOT = os.path.dirname(os.path.abspath(__file__))



def make_matrix(row_strings, size):
    matrix = [[None] * size[1] for i in range(size[0])]
    for i, row in enumerate(row_strings):
        for j, letter in enumerate(row):
            matrix[i][j] = letter
    return matrix

'''
def make_words(matrix, words, checked, pos_i, pos_j, n_letters):
    if n_letters == 1:
        return [matrix[pos_i][pos_j]]
    tmp = []
    for i in range(pos_i - 1, pos_i + 2):
        for j in range(pos_j - 1, pos_j + 2):
            if (i < matrix.shape[0]) & (i >= 0) & (j < matrix.shape[1]) & (j >= 0) & ((i, j) not in checked):
                for elem in make_words(matrix, words, checked + [(i, j)], i, j, n_letters - 1):
                    tmp.append(matrix[pos_i][pos_j] + elem)
    return words + tmp
'''

'''def make_words(matrix, words, wordpaths, checked, pos_i, pos_j, n_letters, postfixes):
    if n_letters == 1:
        return [matrix[pos_i][pos_j]], [[(pos_i, pos_j)]]
    tmp_words = []
    tmp_paths = []
    for i in range(pos_i - 1, pos_i + 2):
        for j in range(pos_j - 1, pos_j + 2):
            if (i < matrix.shape[0]) & (i >= 0) & (j < matrix.shape[1]) & (j >= 0) & ((i, j) not in checked):
                w, p = make_words(matrix, words, wordpaths, checked + [(i, j)], i, j, n_letters - 1, postfixes)
                for elem, path in zip(w, p):
                        if (len(postfixes) > len(matrix[pos_i][pos_j] + elem)) &\
                            ((matrix[pos_i][pos_j] + elem) in postfixes[len(matrix[pos_i][pos_j] + elem) - 1]):
                        tmp_paths.append([(pos_i, pos_j)] + path)
                        tmp_words.append(matrix[pos_i][pos_j] + elem)
    return words + tmp_words, wordpaths + tmp_paths
'''
def make_words(matrix, pos_i, pos_j, n_letters, prefixes):
    words = [[(matrix[pos_i][pos_j], [(pos_i, pos_j)])]]
    for k in range(n_letters - 1):
        tmp = []
        for word in words[-1]:
            str = word[0]
            path = word[1]
            pos_i = path[-1][0]
            pos_j = path[-1][1]
            for i in range(pos_i - 1, pos_i + 2):
                for j in range(pos_j - 1, pos_j + 2):
                    if (i < matrix.shape[0]) & (i >= 0) & (j < matrix.shape[1]) & (j >= 0) & ((i, j) not in path):
                        if ((str + matrix[i][j]) in prefixes[len(str + matrix[i][j]) - 1]):
                            tmp.append((str + matrix[i][j], path + [(i, j)]))
        words.append(tmp)
    return words


'''def get_all_words(matrix, postfixes, n_letters):
    all_words = []
    all_paths = []
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            words, wordpaths = make_words(matrix, [], [], [(i, j)], i, j, n_letters, postfixes)
            all_words += words
            all_paths += wordpaths
    return all_words, all_paths
'''

def get_all_words(matrix, prefixes, n_letters):
    all_words = [None] * n_letters
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            words = make_words(matrix, i, j, n_letters, prefixes)
            for k in range(n_letters):
                if all_words[k] == None:
                    all_words[k] = words[k]
                else:
                    all_words[k] += words[k]
    return all_words

def get_dictionary(dictionary_path):
    with open(dictionary_path, 'r') as fdict:
        return get_set_of_words(fdict.read())

def get_set_of_words(dict_txt):
    diffs = [word.lower() for word in re.split("[^А-Я]", dict_txt) if len(word) > 1]
    dict = set()
    for word in diffs: dict.add(word)
    return dict


def find_words(words, dict, targets):
    found = []
    paths = list(words.values())
    for i, word in enumerate(words.keys()):
        if word in dict:
            cost = 0
            for j, target in enumerate(targets):
                if target in paths[i]:
                    cost += len(targets) - j
            found.append((word, paths[i], cost))
    return found



def visualization(found, matrix):
    print("\nWords which were found:\n")
    for word, path, cost in found:
        print(" \033[34;48m" + word + "\033[m ")
        for i in range(matrix.shape[0]):
            tmp = ""
            for j in range(matrix.shape[1]):
                if (i, j) in path:
                    tmp += " \033[31;48m" + matrix[i][j] + "\033[m "
                else:
                    tmp += ' ' + matrix[i][j] + ' '
            print(tmp)
        print("\n")

def cls():
    os.system(['clear','cls'][os.name == 'nt'])

def get_postfixes(dict, length):
    postfixes = set()
    for word in dict:
        if len(word) >= length:
            postfixes.add(word[-length:])
    return postfixes

def get_prefixes(dict, length):
    prefixes = set()
    for word in dict:
        if len(word) >= length:
            prefixes.add(word[:length])
    return prefixes


def get_words(letters):

    row_strings = textwrap.wrap(letters, 5)
    print(row_strings)

    targets = [(4, 3), (3, 1)]
    matrix = np.array(make_matrix(row_strings, size=(5, 5)))
    print(matrix)

    DICT_PATH = os.path.join(ROOT, 'dictionary.txt')
    dict = get_dictionary(DICT_PATH)

    prefixes = []
    for l in range(19):
        prefixes.append(get_prefixes(dict, l + 1))

    words = get_all_words(matrix, prefixes, n_letters=17)
    all_words = []
    for l in range(17):
        tmp = defaultdict(list)
        for word in words[l]:
            tmp[word[0]] = word[1]
        found = find_words(tmp, dict, targets)
        all_words += found
    print(len(all_words))
    #print(all_words[:10])

    return all_words




if __name__ == '__main__':

    row_strings = ["икывл", "ннчтк", "оеаьа", "зкннв", "есйит"]
    targets = [(4, 3), (3, 1)]
    matrix = np.array(make_matrix(row_strings, size=(5, 5)))
    print(matrix)

    DICT_PATH = os.path.join(ROOT, 'dictionary.txt')
    dict = get_dictionary(DICT_PATH)

    prefixes = []
    for l in range(19):
        prefixes.append(get_prefixes(dict, l + 1))

    words = get_all_words(matrix, prefixes, n_letters=17)
    all_words = []
    for l in range(17):
        tmp = defaultdict(list)
        for word in words[l]:
            tmp[word[0]] = word[1]
        found = find_words(tmp, dict, targets)
        all_words += found
    print(len(all_words))

############################################################################################################

    '''
    postfixes = []
    for l in range(10):
        postfixes.append(get_postfixes(dict, l + 1))
    '''


    prefixes = []
    for l in range(19):
        prefixes.append(get_prefixes(dict, l + 1))

    words = get_all_words(matrix, prefixes, n_letters=17)
    all_words = []
    for l in range(17):
        tmp = defaultdict(list)
        for word in words[l]:
            tmp[word[0]] = word[1]
        found = find_words(tmp, dict, targets)
        all_words += found
    print(len(all_words))
    visualization(all_words, matrix)

    '''
    length = [6, 7, 5, 8]
    for l in length:
        words = defaultdict(list)
        all_words, all_paths = get_all_words(matrix, postfixes, n_letters=l)
        for i, word in enumerate(all_words):
            words[word] = all_paths[i]

        found = find_words(words, dict, targets)
        found.sort(key=lambda item: -item[2])
        found = map(lambda x: (x[0], x[1]), found)

        visualization(found, matrix)
    '''




# -*- coding: utf-8 -*-

import sys
import re
import itertools


def get_words(file_name):
    f = open(file_name, 'r')
    file_text = f.read()
    f.close()
    words = []
    pattern = re.compile("(([\w]+[-'])*[\w']+'?)", re.U)
    text = unicode(file_text, 'utf8')
    text = text.replace('--', ' -- ')
    for token in text.split():
        m = pattern.match(token)
        if m:
            words.append(m.group())
    return words


def get_shingles(words, shingle_size):

    words_count = len(words)
    shingles = []

    if words_count < shingle_size:
        return shingles

    for i in range(0, words_count - shingle_size + 1):
        shingle = ""
        for j in range(i, i + shingle_size):
            shingle += words[j]
        shingles.append(shingle)

    return shingles


def get_word_hash_function(p, word):
    hash_value = 0
    p_pow = 1
    for i in range(0, len(word)):
        hash_value += ord(word[i]) * p_pow
        p_pow *= p
    return hash_value


def get_hash_functions_matrix(shingles):
    hash_functions_matrix = []
    previous_percentage = -1

    hash_length = 84

    for p in range(1, hash_length + 1):
        hash_functions = []
        for shingle in shingles:
            hash_functions.append(get_word_hash_function(p + 10, shingle))
        hash_functions_matrix.append(hash_functions)
        percentage = 100 * p / hash_length
        if percentage != previous_percentage:
            print str(percentage) + "% done"
            previous_percentage = percentage

    return hash_functions_matrix


def get_minimums(hash_matrix):
    minimums = []
    for row in hash_matrix:
        minimums.append(min(row))
    return sorted(minimums)


def get_super_shingles(minimums):
    super_shingles = []
    super_shingle_size = 14
    count = len(minimums) / super_shingle_size

    for idx in range(0, count):
        super_shingles.append(minimums[idx * super_shingle_size: (idx + 1) * super_shingle_size])

    return super_shingles


def get_text_shingles_minimums(text_file_name):
    print ""
    print "Input file name: " + text_file_name
    print "Getting words..."
    words = get_words(text_file_name)
    print "Got " + str(len(words)) + " words"
    shingles_count = 10
    print "Getting shingles..."
    shingles = get_shingles(words, shingles_count)
    print "Got " + str(len(shingles)) + " shingles"
    print "Getting hash functions..."
    matrix = get_hash_functions_matrix(shingles)
    print "Getting minimums..."
    minimums = get_minimums(matrix)
    print "Got " + str(len(minimums)) + " minimums"
    return minimums


def compare_arrays(operand1, operand2):
    index1 = 0
    index2 = 0

    size1 = len(operand1)
    size2 = len(operand2)

    match_count = 0
    while index1 < size1 and index2 < size2:
        if operand1[index1] == operand2[index2]:
            match_count += 1
            index1 += 1
            index2 += 1
        elif operand1[index1] < operand2[index2]:
            index1 += 1
        else:
            index2 += 1

    percentage = 50 * (size1 + size2) * match_count / (size1 * size2)
    return percentage


def compare_arrays(operand1, operand2):
    index1 = 0
    index2 = 0

    size1 = len(operand1)
    size2 = len(operand2)

    match_count = 0
    while index1 < size1 and index2 < size2:
        if operand1[index1] == operand2[index2]:
            match_count += 1
        index1 += 1
        index2 += 1

    return match_count


def main():

    args_count = len(sys.argv)

    if args_count < 3:
        print "First command line argument must be first input file name"
        print "Second command line argument must be second input file name" 
        return 0

    in_file_name1 = sys.argv[1]
    in_file_name2 = sys.argv[2]

    minimums1 = get_text_shingles_minimums(in_file_name1)
    minimums2 = get_text_shingles_minimums(in_file_name2)

    print "Texts are the same on " + str(compare_arrays(minimums1, minimums2)) + "%"

    super_shingles_1 = get_super_shingles(minimums1)
    super_shingles_2 = get_super_shingles(minimums2)

    print "Matched super shingles count: " + str(compare_arrays(super_shingles_1, super_shingles_2))

    mega_shingles_1 = list(itertools.combinations(super_shingles_1, 2))
    mega_shingles_2 = list(itertools.combinations(super_shingles_2, 2))

    print "Matched mega shingles count: " + str(compare_arrays(mega_shingles_1, mega_shingles_2))

main()

# -*- coding: utf-8 -*-

import sys
import re
import hashlib
import json


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
        shingle = []
        for j in range(i, i + shingle_size):
            shingle.append(words[j])
        shingles.append(shingle)

    return shingles


def get_hash_functions(shingle):
    hash_functions = []

    #1
    digest = hashlib.md5(json.dumps(shingle, sort_keys=True)).hexdigest()
    hash_functions.append(int(digest, hashlib.md5().digest_size))

    #2
    digest = hashlib.sha1(json.dumps(shingle, sort_keys=True)).hexdigest()
    hash_functions.append(int(digest, hashlib.md5().digest_size))

    #3
    digest = hashlib.sha224(json.dumps(shingle, sort_keys=True)).hexdigest()
    hash_functions.append(int(digest, hashlib.md5().digest_size))

    #4
    digest = hashlib.sha256(json.dumps(shingle, sort_keys=True)).hexdigest()
    hash_functions.append(int(digest, hashlib.md5().digest_size))

    #5
    digest = hashlib.sha384(json.dumps(shingle, sort_keys=True)).hexdigest()
    hash_functions.append(int(digest, hashlib.md5().digest_size))

    #6
    digest = hashlib.sha512(json.dumps(shingle, sort_keys=True)).hexdigest()
    hash_functions.append(int(digest, hashlib.md5().digest_size))

    return hash_functions


def get_hash_functions_matrix(shingles):
    hash_functions_matrix = []
    previous_percentage = -1
    for idx, shingle in enumerate(shingles):
        hash_functions_matrix.append(get_hash_functions(shingle))
        percentage = 100 * idx / len(shingles)
        if percentage != previous_percentage:
            print str(percentage) + "% done"
            previous_percentage = percentage
    return hash_functions_matrix


def get_minimums(hash_matrix):
    minimums = []
    for row in hash_matrix:
        minimums.append(min(row))
    return sorted(minimums)


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

main()

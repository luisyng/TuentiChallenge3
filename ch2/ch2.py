#! /usr/bin/env python
import sys

# Procedure followed: each target word is transformed
# into a list of alphabetically ordered chars. The number of
# letters is taken into account, so if:
# foreach word in dictionary
#     len(word) not in possible_lengths
# we continue with the next word. This improves the efficiency as
# there is no unnecessary string manipulation
# 
# if the word in dictionary is within one of the expected lengths,
# its letters are sorted and it is compared with the target words

# read stdin
def read_stdin():
    # outputs
    dictionary = None
    words = []

    # iterate lines
    i = 0
    for line in sys.stdin:
        # remove comments
	if(line.strip()[0] == '#'):
            continue

        # num cases
        if(i == 0):
            dictionary = line.strip()
        # words
        elif(i > 1):
            words.append(line.strip())
        
        # incr
        i += 1

    return dictionary, words

def look_up(path, target_words, letter_lists, word_lengths):
    # num words
    num_words = len(letter_lists)
  
    # solution initialization
    solution = []
    for i in range(num_words):
        solution.append([])

    # read file
    f = open(path)

    # iterate words in dictionary
    for line in f:
        word = line.strip()
        # only check if wordlength is within the target words'
        if(len(word) not in word_lengths):
            continue
        # print 'word with some length: ', word

        # otherwise iterate and compare target words (different to typed one)
        for i in range(0, num_words):
            if(letter_list(word) == letter_lists[i]
                    and word != target_words[i]):
                solution[i].append(word)

    return solution
           
         
# transform word into a list of char alphabetically ordered
def letter_lists(words):
    letter_lists = []
    for w in words:
        letter_lists.append(letter_list(w))
    return letter_lists

def letter_list(word):
    return sorted(list(word))

# list of number of letters of the word
def word_lengths(words):
    word_lengths = []
    for w in words:
        word_lengths.append(len(w))
    # remove duplicates and sort
    return sorted(list(set(word_lengths)))

def sol_str(sol):
    res = ''
    for i in range(len(sol)):
        res += sol[i] + ' '
    return res.strip()
   
# MAIN
# read stdin
dict_path, words = read_stdin()

# transform each word into a list of char alphabetically ordered
letter_lists = letter_lists(words)

# list of word lengths
word_lengths = word_lengths(words)

# lookup
solutions = look_up(dict_path, words, letter_lists, word_lengths)

for i in range(len(solutions)):
    print words[i], '->', sol_str(sorted(solutions[i]))






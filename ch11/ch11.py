#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re



def solve(pr):   
    # build squares
    sqs = []
    for wr in pr.ws:
        sq = wr_to_sq(wr)
        sqs.append(sq)

    # sum them
    sum_sq = sum_2sq(sqs[0], sqs[1])

    # return letter
    return sq_to_wr(sum_sq)

# word to square
def wr_to_sq(wr):
    # main sq
    sq = Sq(wr[0])

    # if color, finished
    if sq.c is not P:
        return sq
   
    # else, iterate
    passed = [sq]
    wr = wr[1:]

    # iterate
    while(len(passed) > 0):
        (wr, passed) = wr_to_sq_it(wr, passed)

    # return sq
    return sq

# word to square, iteration
def wr_to_sq_it(wr, passed):
    n_passed = []
    for pas in passed:
        for sub in pas.sub:
            # obtain next letter
            (l, wr) = (wr[0], wr[1:])

            # assign it to subsquare
            sub.set_c(l)

            # if passed, save also apart
            if l == P:
                n_passed.append(sub)
    return wr, n_passed

# square to word
def sq_to_wr(sq):

    # if color, finished
    if sq.c is not P:
        return sq.c

    # else, iterate
    wr = P
    passed = [sq]

    # iterate
    while(len(passed) > 0):
        (wr, passed) = sq_to_wr_it(wr, passed)

    # return wr
    return wr

# word to square, iteration
def sq_to_wr_it(wr, passed):
    n_passed = []
    for pas in passed:
        for sub in pas.sub:
            
            # append next letter
            wr = wr + sub.c

            # if passed, save also apart
            if sub.c == P:
                n_passed.append(sub)

    return wr, n_passed

def sum_2sq(sq1, sq2):
    # some is black: black
    if sq1.c is B or sq2.c is B:
        return Sq(B)
    # all are white: white
    if sq1.c is W and sq2.c is W:
        return Sq(W)
    # one is 'p', we return it
    if sq1.c is P and sq2.c is W: return sq1
    if sq2.c is P and sq1.c is W: return sq2
   
    # more than one are 'p', sum them
    res = Sq(P)
    bl = 0
    for i in range(0, 4):
        res.sub[i] = sum_2sq(sq1.sub[i], sq2.sub[i])
        if res.sub[i].c == B: bl += 1
    
    # if all black now, big one!
    if bl == 4: 
        return Sq(B)
        
    # return sum
    return res
    

# read cases
def read_cases():
    # outputs
    cases = []

    # read boards
    for i in range(int(sys.stdin.readline())):

        # list of words
        ws = re.findall("[pbw]+", sys.stdin.readline())

        # create prob and append
        pr = Problem(ws)
        cases.append(pr)

    # return cases
    return cases

# problem
class Problem:
    def __init__(self, ws):
       self.ws = ws

B = 'b' # black
W = 'w' # white
P = 'p' # complex square, uncomplete
U = 'u' # uprocessed -> just to avoid recursively creation of subsquares

class Sq:
    def __init__(self, c):
        self.set_c(c)

    # setter for color. when p, create children
    def set_c(self, c):
        self.c = c
        if c == P:
            self.sub = [Sq(U), Sq(U), Sq(U), Sq(U)]        

    # to string
    def __str__(self):
        if self.c in (b, w, u):
            return self.c
        else: 
            return "(" + self.sub[0].__str__() + ", " + self.sub[1].__str__() + ", "  + self.sub[2].__str__() + ", " + self.sub[3].__str__() + ")" 

# MAIN
# solve
cases = read_cases()

for pr in cases:
    print solve(pr)
    




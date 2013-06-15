#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re


def solve(p):
    # iterate subsequences
    for s in p.sub:

        # obtain subsequence
        sub = p.l[(s[0]-1):(s[1])]
        maxn = 0
        for n in sub:
            maxn = max(maxn, sub.count(n))

        # print max
        print maxn


# read cases
def read_cases():
    # outputs
    cases = []

    # read boards
    for i in range(int(sys.stdin.readline())):

        # N, M
        (N, M) = re.findall("\d+", sys.stdin.readline())

        # sequence
        l = [int(n) for n in re.findall("\d+", sys.stdin.readline())]

        # subsequences
        sub = []
        for i in range(0, int(M)):
            t = [int(n) for n in re.findall("\d+", sys.stdin.readline())]
            sub.append(tuple(t))

        # create prob and append
        p = Problem(N, l, sub)
        cases.append(p)

    # return cases
    return cases

# problem
class Problem:
    def __init__(self, N, l, sub):
       (self.N, self.l, self.sub) = (N, l, sub)


# log_level (0: nothing printed. smaller, higher priority)
min_level = 1

# log will only print message in development phase
def log(lv, msg):
    if lv <= min_level: print msg


# MAIN
# solve
cases = read_cases()

for i, p in enumerate(cases):
    print "Test case #" + str(i+1)
    solve(p)
    




#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re

# Approach: calculate the different combinations of (number of soldiers,
# number of chrematoriums). For each one, the time can easily be 
# predicted using the formula applied below. A chrematorium just 
# multiplies the surivivance time. 

def solve(p):
    # enough money to cover width, we'll be safe forever!
    if p.g / p.s >= p.w:
        return -1

    else:
        max_time = 0
        # iterate possible coms of solds and chrematoriums
        for (ns, nch) in comb_sold_chrem(p):
            # max time without using chrematorium
            sol_t = (p.w * (p.h - 1)) / (p.w - ns) + 1
            # chrematoriums just multiply the resistance time
            sol_and_ch_t = (nch + 1) * sol_t
            max_time = max (max_time, sol_and_ch_t)
        return max_time

# all the combinations of sold / chrem that could be max
def comb_sold_chrem(p):
    max_sold = p.g / p.s
    for ns in range(0, max_sold + 1):
        money_left = p.g - (p.s * ns)
        nch = money_left / p.c
        yield (ns, nch)

# read cases
def read_cases():
    # outputs
    cases = []

    # read boards
    for i in range(int(sys.stdin.readline())):

        # params
        par = re.findall("\d+", sys.stdin.readline())

        # create prob and append
        p = Problem(int(par[0]), int(par[1]), int(par[2]), int(par[3]), int(par[4]))
        cases.append(p)

    # return cases
    return cases

# problem
class Problem:
    def __init__(self, w, h, s, c, g):
       (self.w, self.h, self.s, self.c, self.g) = (w, h, s, c, g)


# log_level (0: nothing printed. smaller, higher priority)
min_level = 1

# log will only print message in development phase
def log(lv, msg):
    if lv <= min_level: print msg


# MAIN
# solve
cases = read_cases()

for p in cases:
    print solve(p)
    




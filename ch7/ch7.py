#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import math
import itertools

DIS_INF = 1000000

# letters from 'A' to 'Z'
ABCD = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
# words from length 2 and 3, removing permutations
W2 = [''.join([x, y]) for x in ABCD for y in ABCD if x <= y]
W3 = [''.join([x, y, z]) for x in ABCD for y in ABCD for z in ABCD if x <= y <= z]
W4 = [''.join([x, y, z, t]) for x in ABCD for y in ABCD for z in ABCD for t in ABCD if x <= y <= z <= t]

class Solver:
    def __init__(self, p):
        self.p = p
        self.max = 0

    # solve problem
    def solve(self):

        # build chmap
        chmap = self.build_char_map()

        # limit word length in dictionary
        max_wl_time = self.p.w - 1
        max_wl_cell_num = self.p.n * self.p.m
        self.max_wl = max_wl = min(max_wl_time, max_wl_cell_num, 15)

        # limit dictionary with set of letters
        _dic = dict()
        prev_len = 0
        for w in dic:
            # limit by word length
            if len(w) > max_wl:
                break
            
            # cut dictionary for each length
            if len(w) > prev_len: 
                prev_len = len(w)
                _dic[prev_len] = []

            # limit by char availability
            for ch, n in dist_let(w).iteritems():
                if len(chmap[ch]) < n:
                    break
            else:
                _dic[len(w)].append(w)
 
        # print dictionary dist before
        print "dic1"
        #for key, _di in _dic.iteritems():
        #    print key, len(_di)
            
        # solutions (key, scores)
        sols = {wl: [] for wl in range(2, max_wl + 1)}
        # reg expressions for invalid word combinations (key: max applicable length)
        not_val = {k: [] for k in range(3, max_wl + 1)}    
    

 


        # afterwards we just check the words contained in the dic, not all the combinations
        for i in range(2, max_wl+1):
            print "wooor", i
            for w in _dic[i]:
                self.check_word(w, not_val, chmap, _dic[i], sols)

        print "aaa4"
 
        # compute solutions
        self.compute_points(sols)

    # check if a word is possible. return cells necessary in the middle to complete, and max score if word is possible
    def check_word(self, w, not_val, chmap, _dc, sols):
        for ch in w:
            # there is not enough quantity for at least one of the characters           
            if w.count(ch) > len(chmap[ch]): 
                not_val[self.max_wl].append(regex(w))
                return
        
        # number of words with combinations of these letters, eg: 'AB' is, 'BA' is not => 1
        combs = comb_in_dic(w, _dc) 

        # calculate min distance of cells, and max score if dis == 1
        (to_compl, max_sc) = self.get_min_dis_and_word_score(chmap, w)

        # dis == 1 and combs > 0, save scores
        if to_compl == 0 and combs > 0:
            sols[len(w)].extend([max_sc] * combs)
        # dis > 1, save regex
        elif 0 < to_compl < DIS_INF:
            ind = min(self.max_wl, to_compl + len(w))
            not_val[ind].append(regex(w))

    # build char map: char -> all the instances of cell
    def build_char_map(self):
        chmap = {chr(i): [] for i in range(ord('A'), ord('Z') + 1)}      
        for row in self.p.b:
            for c in row:
                chmap[c.ch].append(c)
        return chmap

    # get min distance between two caracters. calculate also max
    # score for word if the distance is 1: w2 allowed
    def get_min_dis_and_word_score(self, chmap, w):
        to_compl = DIS_INF
        max_sc = 0
        maps = [chmap[ch] for ch in w]
        for tup in itertools.product(*maps):
            # groups of connected
            groups = []
            
            # iterate elements
            br = False
            for el in tup:
                # if using twice the same element, break, tuple not valid, continue
                if tup.count(el) > 1:
                    br = True
                    break

                # join groups
                groups = self.join_to_groups(groups, el)
            if(br): continue
             
            # only one group: word found!      
            if len(groups) == 1:
                # word in dictionary: compute word score
                score = self.w_score(tup)
                max_sc = max(max_sc, score)
                to_compl = 0
            else: 
                # more than one group: for len = 2 and len = 3 we get the necessary letters to complete a word to filter
                if len(w) == 2:
                    to_compl = distance(tup[0].p, tup[1].p) - 1
                elif len(w) == 3:
                    dis = [distance(tup[0].p, tup[1].p), distance(tup[1].p, tup[2].p), distance(tup[0].p, tup[2].p)]
                    to_compl = sorted(dis)[1]
                    
        return (to_compl, max_sc)

    def join_to_groups(self, groups, el1):
        new_g = []
        g1 = [el1]
        for g2 in groups[:]: 
            for el2 in g2:
                if distance(el1.p, el2.p) == 1:
                    g1.extend(g2) 
                else: 
                    new_g.append(g2) 
        new_g.append(g1)              
        return new_g
                       
    # score of a word
    def w_score(self, cells):
        max_wm = 1
        sc = 0
        for c in cells:
            (c_s, wm) = self.c_score(c)
            sc += c_s
            max_wm = max(max_wm, wm)
        return sc * max_wm + len(cells)

      
    # (score of cell, word modifier)
    def c_score(self, cell):
        return (self.p.s[cell.ch] * cell.cm, cell.wm)

    def compute_points(self, sols):
        max_p = 0
        sol_i = []
        sol_k = []
        mult = [i+1 for i in range(2, self.max_wl)]
        
        # possible indexes
        for k, pts in sols.iteritems():
            if len(pts) > 0: 
                sol_i.append(range(0, len(pts)+1))
                sol_k.append(k)
                # biggest first
                pts.sort()
                pts.reverse()

        print sols

        # possible solutions
        for t in itertools.product(*sol_i):
            # compute time
            time = max(max_p, sum([a * b for a,b in zip(t, mult)]))
            if time <= self.p.w:
                su = []
                for i in range(0, len(sol_k)):
                    su.extend(sols[sol_k[i]][0:t[i]])
                # points for this combination
                pts = sum(su)

                # update max
                self.max = max(pts, self.max)

      
# number of combinations of words of in dictionary
def comb_in_dic(w, _dc):
    count = 0
    for p in perm_with_repetition(w):
        if p in _dc: count += 1
    return count
    
# return permutations excluding repetitions (for w = "AAB", avoid repetition)
def perm_with_repetition(w):
    p_seen = []
    for p in itertools.permutations(w):
        # already seen?
        if p in p_seen: continue
        p_seen.append(p)

        # return p as string
        yield "".join(p)

def regex(w):
    # regex
    reg = []
    for p in perm_with_repetition(w):      
        # build reg for permutation
        r = ""
        for ch in p:
            r += ch + ".*"
        reg.append(r)
    
    # build regex for whole word
    res = ""
    for r in reg:
        res += r + "|" 
    return res[:-1]
        
  
     
def dist_let(w):
    dist = dict()
    for ch in w:
        if ch in dist: dist[ch] += 1
        else: dist[ch] = 1
    return dist

# distance between two cells (dis = 1: adjacent, dis = 2: need one cell to complete word...)
def distance(a, b):
    return max(abs(a[0]-b[0]), abs(a[1]-b[1]))

# read cases
def read_cases():
    # outputs
    cases = []

    # read boards
    for i in range(int(sys.stdin.readline())):

        # char scores
        s_line = sys.stdin.readline()
        s = eval(s_line[:-1])

        # w: duration, n: rows, m:columns 
        w = int(sys.stdin.readline())
        n = int(sys.stdin.readline())
        m = int(sys.stdin.readline())
        
        # iterate rows
        board = []
        for j in range(n):
            line = sys.stdin.readline()
            row = []
            for k in range(m):
                cell = Cell((j, k), line[4*k], int(line[4*k+1]), int(line[4*k+2]))
                row.append(cell)
            board.append(row)

        cases.append(Problem(s, w, n, m, board))
    return cases

# read dict
def read_dic():
    # outputs
    dic = []

    # open file
    f = open("/home/luis/Tuenti/ch7/boozzle-dict.txt")

    # read words
    for l in f:
        dic.append(l[:-1])

    return dic

class Problem:
    def __init__(self, s, w, n, m, b):
        self.s = s
        self.w = w
        self.n = n
        self.m = m
        self.b = b

class Cell:
    def __init__(self, p, ch, x, y):
        self.p = p
        self.ch = ch
        if x == 1:
            self.cm = y
            self.wm = 1
        else:
            self.cm = 1
            self.wm = y            
       


def get_words(arr, i):
    perm = math.factorial(len(arr)) / math.factorial(len(arr) - i)
    for j in range(perm):
        w = ''
        dv = j
        _arr = arr[:]
        for k in range(i):
            ind = dv % len(_arr)
            dv = dv / len(_arr) 
            w += _arr.pop(ind)
        yield w
        

# MAIN
# read cases
dic = read_dic()

# read cases
cases = read_cases()

for p in cases:
    solver = Solver(p)
    solver.solve()
    print solver.max

# print "l2, l3", len(W2), len(W3)	
#d_max = 0
#d_min = 10000
#dist = {i: 0 for i in range(2, 16)}

# print regex("AA")
 
#for i in range(1, 5):
#    for w in get_words(ch, i):
#        if w not in words:
#            print w





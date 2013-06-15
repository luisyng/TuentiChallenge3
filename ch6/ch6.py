#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re

# apprach followed: backtracking. we keep a dictionary map of 
# positions > min_time before. For the currrent position, we 
# calculate the possible single movements we can do until we reach the
# exit or an obstacle. if, when reaching an obstacle, we have been
# there before in less time, the path will not be optimum. if the door
# has already been found by other path and the current path has aleady
# reached that amount, not optimum either. trying all the paths recursivelly
# stopping when some of the previous considerations are found, we find the
# optimum path

# simbols 
ICE = 1
ICE_CH = '·'
OBS = 0
OBS_CH = '#'
ME = 8
ME_CH = 'X'
EXT = 9
EXT_CH = 'O'

# dict
DICT = {ICE_CH: ICE, OBS_CH: OBS, ME_CH: ME, EXT_CH: EXT}

class Solver:
    def __init__(self, p):
        # problem
        self.p = p
        self.min = 1000000 # hope there is not big enough cave ;)
        self.prev_time = dict()

    # solve problem
    def solve(self):
        self.iterate(self.p.pos, 0)
            
    def iterate(self, pos, time):
        # increment stopped time
        time += self.p.t

        # prev
        self.prev_time[pos] = time

        # iterate possible moves
        for (n_pos, st, exit) in self.p.get_pos_moves(pos):
            n_time = time + st / self.p.s
            # exit found
            if exit:
                if n_time < self.min:
                    self.min = n_time
            # not exit
            else:
                # only iterate if we haven't been here (avoid cycles)
                not_in_prev = n_pos not in self.prev_time.keys()
                should_go = (n_time < min) and (not_in_prev or n_time < self.prev_time[n_pos])             
                if should_go:
                    self.iterate(n_pos, n_time)
        

# read cases
def read_cases():
    # outputs
    cases = []

    # read boards
    for i in range(int(sys.stdin.readline())):

        # pos, dim and seconds
        first_line = sys.stdin.readline()
        (w, h, s, t) = tuple(re.findall("\d+", first_line))

        # board and current pos
        board = []
        curr_pos = (-1, -1)

        # iterate rows
        for j in range(int(h)):
            row = []
            k = 0

            # iterate columns (squares)
            for ch in sys.stdin.readline().decode('utf8')[:-1]:
                if ch == ME_CH: 
                    curr_pos = (j, k)
                    row.append(ICE)
                elif ch == u'\xb7': row.append(ICE)
                else: row.append(DICT[ch])
                k += 1
            board.append(row)

        # append
        p = Problem(board, curr_pos, float(s), float(t))
        cases.append(p)

    # return cases
    return cases

class Problem:
    def __init__(self, b, pos, s, t):
       self.b = b
       self.pos = pos
       self.s = s
       self.t = t

    # get the position of the possible moves from the given position (all directions)
    def get_pos_moves(self, ps):
        moves = []
        for di in range(4):
            mv = self.get_pos_moves_dir(ps, di)
            if mv != None: moves.append(mv)        
        return moves
        
    # get the next coordinates for a single step move for a given direction
    def get_next_move_coords(self, x, y, st, di): 
        if di == 0:   return (x, y+st+1) # right
        elif di == 1: return (x, y-st-1) # left
        elif di == 2: return (x+st+1, y) # up
        elif di == 3: return (x-st-1, y) # down

    # get the position of the possible moves from the given position (one direction)
    def get_pos_moves_dir(self, ps, di):
        # number of steps 
        st = -1
        # current position
        (x, y) = (ps[0], ps[1]) 
        # element of next move (ice, obs...)
        next = self.b[x][y]
        # aux coords
        (x0, x1, y0, y1) = (0, 0, 0, 0)

        # move as soon as we are still in ice
        while next == ICE:
            st += 1
            (x0, y0) = (x1, y1) 
            (x1, y1) = self.get_next_move_coords(x, y, st, di)      
            next = self.b[x1][y1]

        # return tuple if obs or exit found
        if st != 0 and next == OBS: return ((x0, y0), st, False)
        if next == EXT: return ((x1, y1), st+1, True)
        return None        


# MAIN
# solve
cases = read_cases()
for p in cases:
    solver = Solver(p)
    solver.solve()
    print int(round(solver.min))




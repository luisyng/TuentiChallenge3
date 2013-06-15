#! /usr/bin/env python
import sys
import re

# Approach followed: in a certain position, we first iterate
# the remaining gems and remove the unreachable ones and the ones
# that is not worth to go for them (maximum number of points will
# be inferior to the current one). After that, we run the algorithm
# recursively for any of the remaining gems. When we detect the end
# of a path, we compute again the maximum number of points

class Solver:
    def __init__(self, b):
        # board
        self.b = b
        self.max = 0

    # solve board
    def solve_board(self):
        # prev distance that will not produce increment
        prev = (-1, -1)

        # copy of initial pos, total seconds and gems from the board
        self.explore_path(b.pos, prev, b.t_secs, b.gems[:], 0)


    # recursive method to explore paths
    def explore_path(self, pos, prev, sec_left, gems, points):

        # remove unreachable gems
        self.remove_gems(pos, prev, sec_left, gems, points)

        # no possible gems: end of path
        if len(gems) == 0:
            if points > self.max:
                self.max = points
            return

        for g in gems:
            # calculate distance
            dis = distance(pos, g.pos, prev)          

            # remove gem
            new_gems = gems[:]
            new_gems.remove(g)
 
            # explore new path
            self.explore_path(g.pos, pos, sec_left - dis, new_gems, points + g.val)            

    # remove gems
    def remove_gems(self, pos, prev, secs, gems, points):
        for g in gems[:]:
            dis = distance(pos, g.pos, prev)          
            # unreachable
            if dis > secs:
                gems.remove(g)
            # dis 1 and run out of time
            elif dis == secs == 1:
                # if only one left, end of path
                if points + g.val > self.max:
                    self.max = points + g.val 
                gems.remove(g)
            # reachable but not worth it: max possible points smaller than max
            elif points + g.val + 5 * (secs - 1) < self.max:
                gems.remove(g)             

# distance from the current position to a given gem, including the
# increment for invalid paths
def distance(cu, nx, pr):
    return abs(cu[0]-nx[0]) + abs(cu[1]-nx[1]) + incr_alig(cu, nx, pr)

# if the previous position is aligned (and in the middle) with the current position and
# the target gem, we cannot take this path. The solution is increment 2 the 
# distance in that case
def incr_alig(cu, nx, pr):
    if ((cu[0] == nx[0] == pr[0] and in_middle(pr[1], cu[1], nx[1])) or
            (cu[1] == nx[1] == pr[1] and in_middle(pr[0], cu[0], nx[0]))):
        return 2
    return 0

# return if a single coordinate t is in the range (x, y) or (y, x)
def in_middle(t, x, y):
    return x < t < y or y < t < x

# read boards
def read_boards():
    # outputs
    boards = []

    # read boards
    for i in range(int(sys.stdin.readline())):
        # Build Board
        b = Board()

        # pos, dim and seconds
        b.dim = eval(sys.stdin.readline())
        b.pos = eval(sys.stdin.readline())
        b.t_secs = int(sys.stdin.readline())

        # gems
        sys.stdin.readline()
        nums = re.findall("\d+", sys.stdin.readline())
        for i in range(len(nums) / 3):
            g = Gem(int(nums[3*i]), int(nums[3*i+1]), int(nums[3*i+2]))
            b.gems.append(g)

        # append
        boards.append(b)

    # return boards
    return boards
 
class Board:
    def __init__(self):
        self.dim = (0, 0)
        self.pos = (0, 0)
        self.t_secs = 0
        self.gems = []

class Gem:
    def __init__(self, x, y, val):
        self.pos = (x, y)
        self.val = val

# MAIN
# solve
boards = read_boards()
for b in boards:
    solver = Solver(b)
    solver.solve_board()
    print solver.max




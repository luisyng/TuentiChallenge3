#! /usr/bin/env python
import sys

# read file
def read_stdin():
    # outputs
    initial = []
    rates = []

    # iterate lines
    i = 0
    for line in sys.stdin:
        # num cases
        if(i == 0):
            num_cases = int(line)
        # initial values
        elif(i % 2 == 1):
            initial.append(int(line))
        # rates
        else:
            rates.append(line_to_list(line))
        
        # incr
        i += 1

    return num_cases, initial, rates

# line as a list of floats
def line_to_list(line):
    float_list = []
    for st in line.split():
        float_list.append(float(st))
    return float_list;

# solve case: we find every local minimum, for each one
# which is the local maximum and multiply the factor by (max/min)
def solve_case(initial, rates):
    factor = 1.0

    # iterate until find solution
    while True:
        current_val = rates[0]
        # check if it's local min
        is_local_min = is_first_local_min(rates)

        # truncate list
        rates = rates[1:]

        # if is local_min, then calculate max
        if(is_local_min):
            # print current_val, ' is local min'
            local_max, rates = get_local_max(rates)
            # print local_max, ' is local max, remaining: ' + str(rates)
            factor *= local_max / current_val

        # result found
        if(len(rates) <= 1):
            return int(round(initial * factor))

# check if is min
def is_first_local_min(rates):
    if(len(rates) <= 1):
        return False
    return rates[0] < rates[1]
    
# get max and truncated list of rates
def get_local_max(rates):
    max_i = 0
    max_val = rates[0]
    for i in range(1, len(rates)):
        # Equal or bigger found
        if(rates[i] >= max_val):
            max_i, max_val = i, rates[i]
        else:
            return max_val, rates[i:] 
    # last one is the max
    return max_val, []
            

# MAIN
# read file
num_cases, initial, rates = read_stdin()

# iterate cases
for i in range(num_cases):
    print solve_case(initial[i], rates[i])



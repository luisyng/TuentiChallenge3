#! /usr/bin/env python
import sys
import struct

# approach: we divide the complete set of numbers
# in containers with size 64. while iterating the list
# of numbers, we save the number of elements detected 
# for that container and the sum of the remaniders of the
# elements detected. after the iteration, if only one 
# element is missing in a container, it can be inferred
# as the sum of all the elements is known. if there are
# more than one missing in any container and unfortunately
# we actually need that value, we iterate the list of numbers
# again and this time we save all the elements of the container

factor = 64 # factor to divide to determine container
sum_cont = 2016 # sum of the modules of a container
num_cont = 33554432 # 2^31 / factor
path = "/home/luis/Tuenti/ch4/integers"

# solve
def solve():
    # outputs
    positions = []

    # iterate lines
    i = 0
    for line in sys.stdin:
        # words
        if(i >= 1):
            positions.append(int(line.strip()))

        # incr 
        i += 1

    return positions
 
def read_numbers(positions):
    # initialize structures
    count = [0] * num_cont
    rest = [0] * num_cont
    
    # read integers file
    f = open(path, "rb")
    byte = f.read(4)
    i = 0
    while byte != "":
        # convert into unsigned integer
        num = struct.unpack('I', byte)[0]
        
        # divide and calculate mod
        div = num / factor
        mod = num % factor

        # save count
        count[div] += 1
        rest[div] += mod

        if i == 100:
            break

        # read next byte
        byte = f.read(4)

    # extract results
    last = 0
    nums = [0] * 101
    # if we need a second round: keep the divisors
    second_round = []
    second_round_pos = []
    k = 0
    for dv in range(num_cont):
        # count elements in the container
        co = count_missing(count[dv])
        if co == 1:
            last += 1
            nums[last] = get_missing(dv, rest[dv])
        # more than one missing in the container
        elif co > 1:
            # we only care if is one of the desired
            for i in range(co):
                if last + i in positions:
                    second_round.append(dv)
                    second_round_pos.append(last)
                    break
            last += co

    # second round
    if len(second_round) != 0:
        
        # read integers file
        f = open(path, "rb")
        byte = f.read(4)
     
        # second round: store all in the numbers of the desired
        # container in a dictionary
        i = 0
        num_dict = {dv: [] for dv in second_round}
        while byte != "":
            # convert into unsigned integer
            num = struct.unpack('I', byte)[0]
        
            # divide and save
            div = num / factor
            mod = num % factor
            if div in second_round:
                 num_dict[div].append(mod)

            # read next byte
            byte = f.read(4)

        # extract missing
        for i, dv in enumerate(second_round):
            # mods we have
            mods = num_dict[dv]
            # mods missing
            miss_mods_set = set(range(factor)) ^ set(mods)
            for k, solut in enumerate(sorted(list(miss_mods_set))):
                # save solutions
                nums[second_round_pos[i]+k+1] = solut

    for sol_pos in positions:
        print nums[sol_pos]

# get missing number (when there is only one missing in a container) 	   
def get_missing(div, mod):
    return (div * factor) + (sum_cont - mod)

# return number of elements missing in a container
def count_missing(count):
    return factor - count
           
# MAIN
# solve
positions = solve()
read_numbers(positions)




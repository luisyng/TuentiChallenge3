#! /usr/bin/env python
import sys
import re
import math

# procedure followed: substitute every scene for a letter in the
# range A-Za-Z to save memory and easily treat it with regular expressions
# this limits each case to 54 scenes (hopes it passes the validation!).
# it deletes some trivial fb-ff like ".A>B.C<B" decreasing the execution
# time considerably. Later, we calculate for each scene which ones are bigger,
# generate the list of possible solutions alternating the list of chronologically 
# ordered scenes and all the permutations of the not chronologically ordered scenes
# and finally truncate the set of solutions using regular expressions

# solve
def solve():
    # outputs
    solution_set = []

    # iterate lines
    i = 0
    for line in sys.stdin:
        if(i > 0):
            # read scenes and substitute by letters
            sc = get_scenes(line)
            #print "scc", sc # letters
            let = get_scenes_letters(sc)
            #print "let", let # letters

            # update line with letters
            line = put_letters_in_line(line, sc)  
            #print "line", line

            cp_line = ''
            while cp_line is not line:
                cp_line = line
                line = remove_inmmediate_fb_ff(line)
            #print "line", line

            # get chronological ordered
            ordd = get_ordered(line)
            #print "ord", ordd
            # if some appears twice: invalid
            if some_twice_cron(ordd):
                solution_set.append([])
                continue

            # restrictions: bigger (later in time) than a certain scene
            # also keep a copy for iteration
            bigger = []
            last_bigger = []
            for j in range(len(let)):
                bigger.append([])
                last_bigger.append([])

            # detect all direct restrictions written in the line
            detect(line, let, bigger)

            # iterate until no more restrictions are found
            while not cmp_bigger(bigger, last_bigger):

                # copy of last restrictions
                copy_bigger(bigger, last_bigger)

                # update resctrictions
                update_restrictions(bigger, let)
            
            # convert restrictions into regular expression
            bigger_re = bigger_to_re(bigger, let)

            # set of not ordered
            not_ordd = list(set(let) ^ set(ordd))
            #print "not ord", not_ordd

            # generate the solutions
            sol_set = generate_solutions(bigger_re, ordd, not_ordd)	

            # replace letters
            replace_letters(sol_set, sc)
            	
            # end: save solutions
            solution_set.append(sol_set)
        
        # incr
        i += 1

    return solution_set

# make a copy of the bigger list
def copy_bigger(bigger, bigger_copy):
    for i in range(len(bigger)):
        bigger_copy[i] = bigger[i][:]

# compare if the bigger list is the same as the copy
def cmp_bigger(bigger, bigger_copy):
    for i in range(len(bigger)):
        if bigger[i] != bigger_copy[i]:
            return False
    return True
            
# update restrictions
def update_bigger(bigger_set, val):
    if(val not in bigger_set):
        bigger_set.append(val), 

# detect cronological ordered, fb and ff
def detect(line, sc, bigger):
    for i in range(len(sc)):
        for j in range(len(sc)):
            if j == i:
                continue
            if re.search("\." + sc[i] + "([\.<>][A-Za-z])*\." + sc[j] + "[\.<>\\n]", line):
                #print "det", sc[i], "cr", sc[j]

                # update bigger 
                update_bigger(bigger[i], sc[j])

            if re.search("\." + sc[i] + "([<>][A-Za-z])*>" + sc[j] + "[\.<>\\n]", line):
                #print "det", sc[i], "ff", sc[j]

                # update bigger
                update_bigger(bigger[i], sc[j])
             
            if re.search("\." + sc[i] + "([<>][A-Za-z])*<" + sc[j] + "[\.<>\\n]", line):
                #print "det", sc[i], "fb", sc[j]

                # update bigger 
                update_bigger(bigger[j], sc[i])

# update restrictions: if a < b and b < c => a < c                    
def update_restrictions(bigger, scenes):
    for i in range(len(scenes)):
        for j in range(len(scenes)):
            for k in range(len(scenes)):
                if (i != j and j != k):
                    if (scenes[j] in bigger[i] and scenes[k] in bigger[j]):
                        update_bigger(bigger[i], scenes[k]) 
                    if (scenes[j] in bigger[i] and scenes[k] in bigger[j]):
                        update_bigger(bigger[i], scenes[k])          
  

# converts the restrictions into a list of regular expressions to truncate solutions
def bigger_to_re(bigger, sc):
    bigger_re = []
    for i in range(len(sc)):
        for j in range(len(sc)):
            if i != j and sc[j] in bigger[i]:
                bigger_re.append(sc[j] + ".*" + sc[i])
    return bigger_re

# get all the possible solutions by permuting
def get_scenes(line):
    return list(set(re.findall("[\w,;: ']+", line)))


def get_scenes_letters(sc):
    let = []
    for i in range(len(sc)):
        # print i, sc[i]
        let.append(pos_to_char(i))
    return let

# char to pos
def pos_to_char(i):
    if i < 26:
        return chr(65 + i)
    else: 
        return chr(97 + i)

# pos to char
def char_to_pos(ch):
    if ord(ch) >= 97:
        return ord(ch) - 97
    else:
        return ord(ch) - 65

# replaces letters with real scenes in a string
def replace_letters(sol_set, sc):
    for j in range(len(sol_set)):
        old = sol_set[j]
        sol_set[j] = ''
        for i in range(len(sc)):
            sol_set[j] += sc[char_to_pos(old[2*i])] + ','
        sol_set[j] = sol_set[j][:-1]

# replaces letters in input line
def put_letters_in_line(line, sc):
    for i in range(len(sc)):
        line = line.replace(sc[i], pos_to_char(i))
    return line
        
# create the set of scenes
def create_set(cron, not_cron):
    sol_set = []
    for it in generate_pos_sol(cron, not_cron):
        sol = ''
        for s in it:
            sol += s + ','
        sol_set.append(sol[:-1])
    return sol_set

# generates possible solutions taking into account cron and not cron
def generate_possible_sols(cron, not_cron):
    for pos in position_insertion(cron, not_cron):
        sol = cron[:]
        for i, in_pos in enumerate(pos):
            sol.insert(in_pos, not_cron[i])        
        yield sol

# calculates positions to insert not ordered items in ordered list
def position_insertion(cron, not_cron):
    pos = math.factorial(len(cron) + len(not_cron)) / math.factorial(len(cron))
    for p in range(pos):
        res = []
        p_div = p
        
        for i in range(len(not_cron)):
            res.append(p_div % (len(cron)+i+1))
            p_div = p_div / (len(cron)+i+1)

        yield res

# create the set of scenes
def generate_solutions(bigger_re, cron, not_cron):
    sol_set = []
    for it in generate_possible_sols(cron, not_cron):
        # generate sol
        sol = ''
        for s in it:
            sol += s + ','
        # check validity
        for b_re in bigger_re:
            if re.search(b_re, sol):
                # print b_re, sol
                break
        else:
            sol_set.append(sol[:-1])
            # don't care if already 2 solutions found
            if len(sol_set) > 1:
                break
    return sol_set

# gets the list of ordered items (.A.B > ["A", "B"]
def get_ordered(line):
    with_dot = re.findall("\.[A-Za-z]", line)
    return [x[1:] for x in with_dot]

# checks pattern .A.B.A > impossible    
def some_twice_cron(ordd):
    return len(ordd) is not len(set(ordd))

# substitutes pattern ".A>B.C<B" by ".A.B.C"
def remove_inmmediate_fb_ff(line):
  for ff in re.findall("\.[A-Za-z]>[A-Za-z]", line):
    i1 = ff[1]
    i2 = ff[3]
    for ff2 in re.findall(ff + ".[A-Za-z]<" + i2, line):
        i3 = ff2[5]
        line = re.sub(ff2, "." + i1 + "." + i2 + "." + i3, line)
  return line	
    

           
# MAIN
# solve
solution_set = solve()

# iterate solutions
for sol in solution_set:
    if len(sol) == 0:
        print "invalid"
    elif len(sol) == 1:
        print sol[0]
    else:
        print "valid"



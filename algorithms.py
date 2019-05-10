import copy
import pickle
import random
import time
from random import shuffle

import numpy as np

from solution import Solution
from utils import legal_request, no_overlaps, save_output


'''
Greedy algorithm for group substitutions:
    Iterate through each request
    If all constraints and conditions are satisfied make the substitution
    repeat n times (cause some previous invalid requests are valid now after some
    substitutions are made)
'''
def greedy_search(requests, done_substitutions, sts, ag, overlaps, limits):
    counter = 0
    repeats = 10

    for i in range(repeats):
        for row in requests:
            s_id = row[0]
            a_id = row[1]
            r_id = row[2]

            if a_id not in sts[s_id].activities:  # student does not attend this activity, skip it
                continue
            if sts[s_id].new_groups[a_id] is not None:  # sub for (student, activity) pair is already made
                continue

            if not legal_request(s_id, a_id, r_id, sts, limits, ag, overlaps, soft=True):
                continue

            # all conditions are satisfied, make the substitution
            counter += 1
            current_group = sts[s_id].activities[a_id]
            done_substitutions.append((s_id, a_id, r_id))
            sts[s_id].new_groups[a_id] = current_group
            sts[s_id].activities[a_id] = r_id
            limits[current_group].remove()
            limits[r_id].add()
        print("Greedy search pass:", str(i+1), ", requests:", counter)


'''
After greedy approach, we can't make any more requests.
But we can look if there are requests and examples between pair of students
where each of them wants to go to another's one group and grant both requests and thus
make two substitutions at once
'''
def direct_swaps(requests, done_substitutions, sts, ag, overlaps, limits):
    for row in requests:
        s_id = row[0]
        a_id = row[1]
        r_id = row[2]

        if a_id not in sts[s_id].activities:  # student does not attend this activity, skip it
            continue
        if sts[s_id].new_groups[a_id] is not None:  # sub for (student, activity) pair is already made
            continue
        current_group = sts[s_id].activities[a_id]
        if not legal_request(s_id, a_id, r_id, sts, limits, ag, overlaps):
            if r_id in limits and (not limits[r_id].canAdd()) and \
                    no_overlaps(s_id, r_id, current_group, sts, ag, overlaps):
                for tmp in requests:
                    st = tmp[0]
                    at = tmp[1]
                    rt = tmp[2]
                    if at not in sts[st].activities:
                        continue
                    wanted = sts[st].activities[at]

                    if wanted != r_id:  # groups must be the same
                        continue
                    if rt != current_group:
                        continue

                    if at not in sts[st].activities:
                        continue
                    if sts[st].new_groups[at] is not None:
                        continue
                    if no_overlaps(st, rt, wanted, sts, ag, overlaps):
                        done_substitutions.append((s_id, a_id, r_id))
                        done_substitutions.append((st, at, rt))

                        sts[s_id].new_groups[a_id] = current_group
                        sts[s_id].activities[a_id] = r_id

                        sts[st].new_groups[at] = wanted
                        sts[st].activities[at] = rt

                        limits[current_group].remove()
                        limits[r_id].add()

                        limits[rt].add()
                        limits[wanted].remove()
                        break
    print("After direct swaps requests:", len(done_substitutions))


# probability formula used for Simulated Annealing
def probability(T):
    return np.exp(-1 / T)


# One greedy iteration inside simulated annealing
def alg_iteration(forbidden, zamjene, limits, sts, requests, ag, overlaps):
    for i in range(5):
        for row in requests:

            s_id = row[0]
            a_id = row[1]
            r_id = row[2]

            if (s_id, r_id) in forbidden: # forbidden substitution
                continue
            if a_id not in sts[s_id].activities:
                continue
            if sts[s_id].new_groups[a_id] is not None:
                continue

            if not legal_request(s_id, a_id, r_id, sts, limits, ag, overlaps):
                continue

            zamjene.append((s_id,a_id,r_id))

            current_group = sts[s_id].activities[a_id]
            sts[s_id].new_groups[a_id] = current_group
            sts[s_id].activities[a_id] = r_id

            limits[current_group].remove()
            limits[r_id].add()


'''
- Main algorithm of this optimization procedure
- Hybrid algorithm - combination simulated annealing algorithm and tabu algorithm
- main idea: by removing some substitution(request) in current solution maybe we can free space for one 
  or more better substitutions. We ignore removed substitution when looking for new valid substitutions (tabu)
  If we get better solution, we accept it, otherwise we stochastically decide whether we will accept it or not.
  If we accept worse solution, now we remove another substitution(request) from done substitutions (we have a list of 
  removed solutions). By doing this we can succesfully avoid local optimums and find areas with better solutions. 
  The constant improvement of the solution over time is in favor of this thesis.
'''
def SA(requests,obavljene_zamjene,sts,ag,overlaps,limits,students,args,start,T_0 = 3,alpha=0.96):
    award_activity = list(map(int,args.award_activity.split(",")))
    minmax_penalty = args.minmax_penalty
    award_student = args.award_student
    timeout = args.timeout
    T = T_0
    s_best = Solution(limits=pickle.loads(pickle.dumps(limits)), sts=pickle.loads(pickle.dumps(sts)),
                      obavljene_zamjene=obavljene_zamjene.copy(), students=students, penalty=minmax_penalty, award_activity=award_activity, award_student=award_student)
    current_solution = copy.deepcopy(s_best)
    best_fitness = s_best.fitness()
    current_fitness = best_fitness
    milenial_fitness = best_fitness
    forbidden = []
    i = 0
    while True:
        flag = True # request is successfully deleted
        s_prime = pickle.loads(pickle.dumps(current_solution))
        s = None
        a = None
        g = None

        if time.time()-start > (timeout+20):
            if timeout == 600:
                save_output(s_best, args.dir, timeout, args.dir + args.students_file)
                timeout = 1800
            elif timeout == 1800:
                save_output(s_best, args.dir, timeout, args.dir + args.students_file)
                timeout = 3600
            else:
                break

        final = current_solution.scoreA()
        for _ in range(final):

            s, a, g = random.choice(s_prime.obavljene_zamjene)
            initial_group = s_prime.sts[s].new_groups[a]

            if legal_request(s, a, initial_group, s_prime.sts, s_prime.limits, ag, overlaps):
                flag = False
                forbidden.append((s,g))
                s_prime.limits[g].remove()
                s_prime.limits[initial_group].add()

                s_prime.obavljene_zamjene.remove((s,a,g))

                s_prime.sts[s].activities[a] = initial_group
                s_prime.sts[s].new_groups[a] = None
                break
        if flag:  # if we can't remove any sub, break the loop
            break
        alg_iteration(forbidden, s_prime.obavljene_zamjene, s_prime.limits, s_prime.sts, requests, ag, overlaps)
        prime_fitness = s_prime.fitness()

        if prime_fitness >= current_fitness:
            forbidden = []
            current_solution = s_prime
            current_fitness = prime_fitness
        elif random.uniform(0,1) < probability(T):
            current_solution = s_prime
            current_fitness = prime_fitness
        else:
            forbidden = []

        if current_fitness > best_fitness:
            s_best = current_solution
            best_fitness = current_fitness
        if i % 1500 == 0:
            if milenial_fitness == best_fitness:
                T = T_0
            else:
                milenial_fitness = best_fitness

        if i%1000 == 0:
            shuffle(requests)
        if i%200 == 0:
            T = T*alpha
        i += 1


    print("End of algoritm - Number of evaluation calls:", Solution.counter, ", Final fitness:", best_fitness)
    return s_best

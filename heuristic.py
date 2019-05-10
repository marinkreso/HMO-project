import time
import argparse
from algorithms import *
from utils import *


'''
Optimization procedure
'''
def algorithm(args):
    # parsing paths to files
    start = time.time()
    path = args.dir
    student_path = path+args.students_file
    limit_path = path+args.limits_file
    request_path = path+args.requests_file
    overlaps_path = path+args.overlaps_file
    output_file = path+args.output_file

    # loading and parsing files into memory
    student_file = load_file(student_path)
    limit_file = load_file(limit_path)
    requests = load_file(request_path)
    # shuffle(requests) #to make our algorithm more robust and stochastic
    overlaps_file = load_file(overlaps_path)

    # One pass through request to get further insight for optimization of swaps
    groups, students = preparation_step(requests)

    # Initialization of needed variables
    obavljene_zamjene = []
    sts = load_students(student_file)
    ag = load_ag(student_file) # to know activity for each group
    limits = load_limits(limit_file)
    overlaps = load_overlaps(overlaps_file)

    # greedy_search with multiple iterations
    print("Total number of requests:",len(requests))
    greedy_search(requests, obavljene_zamjene, sts, ag, overlaps, limits)

    # doing direct swaps
    direct_swaps(requests, obavljene_zamjene, sts, ag, overlaps, limits)

    # simulated annealing
    best = SA(requests.copy(), obavljene_zamjene, sts, ag, overlaps, limits, students, args, start)

    prelazi = dict()
    for s,a,g in best.obavljene_zamjene:
        prelazi[s+a] = g

    # save the results
    csv_file= open(student_path)
    csv_reader = csv.reader(csv_file, delimiter=',')
    csv_reader = list(csv_reader)
    myFile = open(output_file, 'w')  
    with myFile:
        writer = csv.writer(myFile)
        for row in csv_reader:
            key = row[0]+row[1]
            if key in prelazi:
                writer.writerow([row[0],row[1],row[2],row[3],prelazi[key]])
            else:
                writer.writerow(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--timeout', type=int, default=600, help = "Time in seconds after which program stops executing")
    parser.add_argument('--award_activity', type=str, default="1,2,3,4,5", help = "Bonus points for number of activities swap is made")
    parser.add_argument('--award_student',type=int,default=1)
    parser.add_argument('--minmax_penalty',type=int,default=1)
    parser.add_argument('--students_file',type=str,default="student.csv")
    parser.add_argument('--requests_file',type=str,default="requests.csv")
    parser.add_argument('--limits_file',type=str,default="limits.csv")
    parser.add_argument('--overlaps_file',type=str,default="overlaps.csv")
    parser.add_argument('--output_file',type=str,default="output.csv")
    parser.add_argument('--dir',type=str,default="./")
    args = parser.parse_args()
    
    algorithm(args)


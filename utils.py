import csv

from limit import Limit
from student import Student


# returns parsed csv file as a list. Headers are skipped
def load_file(path):
    csv_file = open(path)
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)
    return list(csv_reader)


# returns map of students
def load_students(data):
    students = dict()
    for row in data:
        student_id = row[0]
        if student_id not in students:
            students[student_id] = Student()
        students[student_id].add_activity(row[1], row[2], row[3])
    return students


def load_ag(data):
    ag = dict()
    for row in data:
        ag[row[3]] = row[1]
    return ag


def load_limits(data):
    limits = dict()
    for row in data:
        limits[row[0]] = Limit(row[1], row[2], row[3], row[4], row[5])
    return limits


def load_overlaps(data):
    overlaps = dict()
    for row in data:
        group1 = row[0]
        group2 = row[1]
        if group1 not in overlaps:
            overlaps[group1] = [group2]
        else:
            overlaps[group1].append(group2)
    return overlaps


def legal_request(s_id, a_id, r_id, sts, limits, ag, overlaps, soft=False):
    current_group = sts[s_id].activities[a_id]

    if r_id not in limits or current_group not in limits:
        return False

    return limits[current_group].canRemove(soft) and limits[r_id].canAdd(soft) and \
           no_overlaps(s_id, r_id, current_group, sts, ag, overlaps)


def no_overlaps(s_id, requested_group, current_group, sts, ag, overlaps):
    if requested_group not in overlaps:
        return True

    groups = sts[s_id].activities.values()

    for g in groups:
        if g in overlaps[requested_group]:
            if g not in ag.keys() or requested_group not in ag.keys() :
                return False
            if ag[g] == ag[requested_group]:
                continue
            return False
    return True


def preparation_step(requests):
    groups = dict()
    students = dict()
    for row in requests:
        s_id = row[0]
        a_id = row[1]
        r_id = row[2]
        if r_id not in groups:
            groups[r_id] = [(s_id, a_id)]
        else:
            groups[r_id].append((s_id, a_id))
        if s_id+a_id not in students:
            students[s_id+a_id] = [r_id]
        else:
            students[s_id+a_id].append(r_id)

    return groups, students


def save_output(best, output_dir, timeout, student_path):
    prelazi = dict()
    for s, a, g in best.obavljene_zamjene:
        prelazi[s+a] = g

    csv_file= open(student_path)
    csv_reader = csv.reader(csv_file, delimiter=',')
    csv_reader = list(csv_reader)
    myFile = open(output_dir+str(timeout)+".csv", 'w')
    with myFile:
        writer = csv.writer(myFile)
        for row in csv_reader:
            key = row[0]+row[1]
            if key in prelazi:
                writer.writerow([row[0],row[1],row[2],row[3],prelazi[key]])
            else:
                writer.writerow(row)
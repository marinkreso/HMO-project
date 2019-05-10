# class that represents a student
class Student:
    def __init__(self):
        self.activities = dict()
        self.weights = dict()
        self.new_groups = dict()

    def add_activity(self,activity,weight,group):
        self.activities[activity] = group
        self.weights[activity] = weight
        self.new_groups[activity] = None
# Class that represents upper and lower limits of each group
class Limit:
    def __init__(self,students_cnt,_min,min_p,_max,max_p):
        self.cnt = int(students_cnt)
        self.min = int(_min)
        self.minP = int(min_p)
        self.max = int(_max)
        self.maxP = int(max_p)

    def add(self):
        self.cnt += 1

    def remove(self):
        self.cnt -= 1

    def canAdd(self,soft=False):
        if soft:
            return self.cnt < self.maxP
        else:
            return self.cnt < self.max

    def canRemove(self,soft=False):
        if soft: 
            return self.cnt > self.minP
        else:
            return self.cnt > self.min

    def space_left(self):
        return self.max-self.cnt

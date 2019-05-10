# class that represents one solution of algorithm
class Solution:
    counter = 0

    def __init__(self,obavljene_zamjene,limits,sts,students,award_student,award_activity,penalty):
        self.obavljene_zamjene = obavljene_zamjene
        self.limits = limits
        self.sts = sts
        self.award = award_activity
        self.award_student = award_student
        self.penalty = penalty
        self.amax = len(self.award)
        self.students = students

    def fitness(self,hard=True):
        Solution.eval_number()
        if hard:
            return self.hard_fitness()
        else:
            return len(self.obavljene_zamjene)

    def hard_fitness(self):
        return self.scoreA()+self.scoreB()+self.scoreC()-self.scoresDE()

    def normal_fitness(self):
        return self.scoreA()+self.scoreB()+self.scoreC()-self.scoresDE()
    
    def scoreA(self):
        return len(self.obavljene_zamjene)
    
    def alternateA(self):
        counter = 0
        for s,elem in self.sts.items():
            for a,g in elem.weights.items():
                if self.sts[s].new_groups[a] is not None:
                    counter +=int(g)
        return counter

    def scoreC(self):
        scoreC = 0
        for s,elem in self.sts.items():
            all_done = True
            for a,g in elem.new_groups.items():
                if s+a not in self.students:
                    continue
                if g is None:
                    all_done = False
                    break
            
            if all_done:
                scoreC +=self.award_student
        return scoreC

    def scoreB(self):
        scoreB = 0
        for st in self.sts.values():
            changes = 0
            for activity in st.new_groups.values():
                if activity is not None:
                    changes +=1
            if changes > 0:
                changes = min(self.amax,changes)
                scoreB += self.award[changes-1]
        return scoreB

    def scoresDE(self):
        suma_iznad = 0
        suma_ispod = 0
        for limit in self.limits.values():
            if limit.cnt > limit.maxP:
                suma_iznad += (limit.cnt-limit.maxP)*self.penalty
            if limit.cnt < limit.minP:
                suma_ispod += (limit.minP-limit.cnt)*self.penalty
        return suma_ispod+suma_iznad

    @classmethod
    def eval_number(cls):
        cls.counter +=1

from random import random


class CSP(object):
    """
    This object defines our Constraint Satisfaction Problem
    """
    def __init__(self, n):
        self.n = n

        """
        Start with a random guess
        """
        temp = [i for i in range(n)]
        for i in range(n):
            j = int(random()*i)
            temp[i], temp[j] = temp[j], temp[i]
        self.solution = temp
        self.conflicts = [None]*self.n
        self.conflicts_stale = True

    def findConflicts(self):
        if not self.conflicts_stale:
            return self.conflicts

        for i in range(self.n):
            self.conflicts[i] = self.getHits(i, self.solution[i])

        self.conflicts_stale = False
        return self.conflicts

    def getHits(self, col, row):
        hits = 0
        for i in range(self.n):
            if i == col:
                continue
            if self.solution[i] == row:
                hits += 1
            if self.solution[i] == i - col + row:
                hits += 1
            if self.solution[i] == -i + col + row:
                hits += 1
        return hits

    def minimizeConflicts(self):
        conflicts = self.findConflicts()

        col = int(random() * len(conflicts))
        while conflicts[col] == 0:
            col = int(random() * len(conflicts))

        leastConflicts = float("inf")
        best = []
        for i in range(self.n):
            conflicts = self.getHits(col, i)
            if conflicts < leastConflicts:
                leastConflicts = conflicts
                best = [i]
            elif conflicts == leastConflicts:
                best.append(i)

        self.solution[col] = best[int(random() * len(best))]

        self.conflicts_stale = True


def minConflicts(csp, maxSteps):
    """
    Looks for an optimal solution.
    Returns False of none is found within the maximum number of steps.
    """
    for steps in range(maxSteps):
        conflicts = csp.findConflicts()

        totalConflicts = 0
        for j in range(len(conflicts)):
            totalConflicts += conflicts[j]

        if totalConflicts == 0:
            return csp.solution

        csp.minimizeConflicts()
    return False


def printSolution(solution):
    """
    Renders the solution as a grid
    """
    if not solution:
        print "No solution was found"
    else:
        output = ""
        for i in range(len(solution)):
            for j in range(len(solution)):
                output += "+---"
            output += "+\n"
            for j in range(len(solution)):
                output += "| Q " if solution[i] == j else "|   "
            output += "|\n"
        for i in range(len(solution)):
            output += "+---"
        output += "+\n\n"
        print output

maxIterations = 1000
csp1 = CSP(8)
csp2 = CSP(1000)

best = minConflicts(csp1, maxIterations)
printSolution(best)

best = minConflicts(csp2, maxIterations)
printSolution(best)

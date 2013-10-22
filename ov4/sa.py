from collections import deque
import math
from random import random, randint
from copy import deepcopy


class SA(object):
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.checked_states = []

    def generate_start_state(self):
        return [[False]*self.n for i in range(self.n)]

    def objective(self, state):
        optimum = self.n*self.k*1.0
        cell_count = 0
        for row in state:
            for cell in row:
                if cell:
                    cell_count += 1
        overflow_count = 0
        for row in state:
            overflow_count += max(0, sum(row)-self.k)
        for col in zip(*state[::-1]):
            overflow_count += max(0, sum(col)-self.k)
        for i in range(self.n):
            row_downleft = row_upleft = row_downright = row_upright = 0
            for j in range(self.n):
                if 0 <= i + j < self.n:
                    row_upleft += state[i+j][j]
                    row_downleft += state[self.n - i - j - 1][j]

                    if i != 0:
                        row_upright += state[j][i+j]
                        row_downright += state[self.n - j - 1][i + j]

            overflow_count += max(0, row_downleft - self.k)
            overflow_count += max(0, row_downright - self.k)
            overflow_count += max(0, row_upleft - self.k)
            overflow_count += max(0, row_upright - self.k)

        rating = cell_count/optimum-overflow_count*0.1
        return min(1, max(0, rating))

    def quotient(self, p_max, p):
        p_rate = self.objective(p)
        if p_rate == 0:
            return 0.0
        return (self.objective(p_max) - p_rate)/p_rate

    def generate_neighbors(self, state):
        neighbors = []
        for i in range(len(state)):
            for j in range(len(state[i])):
                new_state = deepcopy(state)
                new_state[i][j] = not state[i][j]
                neighbors.append(new_state)
        return neighbors

    def compare(self, a, b):
        for x in range(len(a)):
            for y in range(len(a)):
                if a[x][y] != b[x][y]:
                    return False
        return True

    def is_checked(self, state):
        for checked_state in self.checked_states:
            if self.compare(state, checked_state):
                return True
        return False

    def print_board(self, state):
        for row in state:
            row_string = ""
            for cell in row:
                row_string += "1" if cell else "0"
            print row_string

    def run(self):
        start = self.generate_start_state()
        t = 1.0
        queue = deque([start])
        current = None
        while t > 0:
            current = queue.popleft()
            self.checked_states.append(current)
            if self.objective(current) >= 1:
                break
            neighbors = self.generate_neighbors(current)
            n_max = -10e8
            best_neighbor = None
            for neighbor in neighbors:
                if self.is_checked(neighbor):
                    continue
                n_rating = self.objective(neighbor)
                if n_rating > n_max:
                    n_max = n_rating
                    best_neighbor = neighbor
            q = self.quotient(best_neighbor, current)
            probability = min(1, math.exp(-q/t))
            if random() > probability:
                queue.append(best_neighbor)
            else:
                queue.append(neighbors[randint(0, len(neighbors)-1)])
            t -= 0.005
        self.print_board(current)
        print "checked states:", len(self.checked_states)
        print "Number of eggs:", sum([sum(row) for row in current])

sa = SA(5, 2)
sa.run()

sa2 = SA(6, 2)
sa2.run()

sa3 = SA(8, 1)
sa3.run()

sa4 = SA(10, 3)
sa4.run()

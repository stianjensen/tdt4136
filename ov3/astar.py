class Astar(object):
    explored_states = {}

    def heuristic(self, node, start, end):
        raise NotImplementedError

    def search(self, start, end):
        openset = set()
        closedset = set()
        openset.add(start)
        while openset:
            current = min(openset, key=lambda o: o.g + o.h)
            if current.isEqual(end):
                path = []
                while current.parent:
                    path.append(current)
                    current = current.parent
                path.append(current)
                return path[::-1]
            current.generate_children()
            openset.remove(current)
            closedset.add(current)
            for node in current.children:
                if node.state not in Astar.explored_states:
                    Astar.explored_states[node.state] = node
                    if node in closedset:
                        continue
                    if node in openset:
                        new_g = current.g + current.move_cost(node)
                        if new_g < node.g:
                            node.g = new_g
                            node.parent = current
                    else:
                        node.g = current.g + current.move_cost(node)
                        node.h = self.heuristic(node, start, end)
                        node.parent = current
                        openset.add(node)
        return None


class Node(object):
    def __init__(self, state):
        self.g = 0
        self.h = 0
        self.parent = None
        self.children = []
        self.state = state

    def move_cost(self, other):
        raise NotImplementedError

    def isEqual(self, other):
        return self.state == other.state

    def genereate_children(self):
        raise NotImplementedError

    def __repr__(self):
        return ",".join([str(i) for i in self.state])

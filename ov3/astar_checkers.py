from astar import Astar, Node


class AstarCheckers(Astar):
    def heuristic(self, node, start, end):
        return 1


class CheckersNode(Node):
    def move_cost(self, other):
        return 1

    def generate_children(self):
        space = self.state.index(None)
        for i, piece in enumerate(self.state):
            if space in (i-2, i-1, i+1, i+2):
                childState = list(self.state)
                childState[space] = piece
                childState[i] = None
                childState = tuple(childState)
                if childState not in AstarCheckers.explored_states:
                    self.children.append(CheckersNode(childState))

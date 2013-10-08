from astar_checkers import AstarCheckers, CheckersNode

Black = 1
Red = -1

startState = tuple(
    [Black if i < 6 else None if i == 6 else Red for i in range(13)]
)
endState = tuple(reversed(startState))

paths = AstarCheckers()
start = CheckersNode(startState)
end = CheckersNode(endState)
path = paths.search(start, end)
if path is None:
    print "No path found"
else:
    print "Path found:", path
    print "Moves:", len(path)-1

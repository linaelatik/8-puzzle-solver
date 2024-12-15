from heapq import heappush, heappop

# Main solvePuzzle function
def solvePuzzle(state, heuristic):
    """
    Solve the n^2-1 puzzle using the A* search algorithm with the specified heuristic.

    Parameters:
        state (list of lists): The initial state of the puzzle.
        heuristic (function): The heuristic function to estimate the cost to reach the goal.

    Outputs:
        tuple: (steps, exp, max_frontier, opt_path, err)
            steps (int): Number of steps to optimally solve the puzzle (excluding the initial state)
            exp (int): Number of nodes expanded to reach the solution
            max_frontier (int): Maximum size of the frontier over the whole search
            opt_path (list): Optimal path from start to goal.
            err (int): Error code (-1 for invalid input, -2 for unsolvable puzzle, 0 for success).
    """
    # Input validation
    if not state or not isinstance(state, list):
        return 0, 0, 0, None, -1  # err = -1
    n = len(state)
    for row in state:
        if len(row) != n:
            return 0, 0, 0, None, -1  # err = -1
        for val in row:
            if not isinstance(val, int):
                return 0, 0, 0, None, -1  # err = -1
    # Check for missing or duplicate tiles
    flattened_state = [num for row in state for num in row]
    expected_numbers = set(range(n * n))
    if set(flattened_state) != expected_numbers:
        return 0, 0, 0, None, -1  # err = -1

    # Check if the puzzle is solvable
    if not is_solvable(state):
        return 0, 0, 0, None, -2  # err = -2 for unsolvable puzzle

    # Initialize the open list (priority queue) and closed set
    open_list = []
    closed_set = set()
    exp = 0  # Nodes expanded
    max_frontier = 0

    # Create the initial node
    initial_node = PuzzleNode(state, cost=0)
    initial_node.fval = heuristic(state) + initial_node.cost
    heappush(open_list, initial_node)
    max_frontier = max(max_frontier, len(open_list))
    goal_state=  get_goal_state(n)

    while open_list:
        # Pop the node with the lowest fval
        current_node = heappop(open_list)
        exp += 1

        # Check if we've reached the goal state
        if PuzzleNode.is_goal(current_node.state, goal_state):
            # Reconstruct the optimal path
            steps = current_node.cost
            opt_path = []
            node = current_node
            while node:
                opt_path.append(node.state)
                node = node.parent
            opt_path.reverse()
            return steps, exp, max_frontier, opt_path, 0  # Success

        # Add the current state to the closed set
        state_tuple = tuple(tuple(row) for row in current_node.state)
        if state_tuple in closed_set:
            continue
        closed_set.add(state_tuple)

        # Generate successors and add them to the open list
        successors = current_node.generate_successors()
        for child in successors:
            child_state_tuple = tuple(tuple(row) for row in child.state)
            if child_state_tuple in closed_set:
                continue
            child.cost = current_node.cost + 1
            child.fval = child.cost + heuristic(child.state)
            heappush(open_list, child)
        # Update the maximum frontier size
        max_frontier = max(max_frontier, len(open_list))

    # If no solution is found, return failure in case it was not detected by is_solvable()
    return 0, exp, max_frontier, None, -1  # No solution found
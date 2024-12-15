def h1(state):
    """
    Heuristic function h1: Calculates the number of misplaced tiles.

    Parameters:
        state (list of lists): The current puzzle state.

    Outputs:
        int: The number of misplaced tiles.
    """
    n = len(state)
    goal_state = get_goal_state(n)
    misplaced = 0
    for i in range(n):
        for j in range(n):
            if state[i][j] != goal_state[i][j] and state[i][j] != 0:
                misplaced += 1
    return misplaced

def h2(state):
    """
    Heuristic function h2: Calculates the total Manhattan distance of tiles from their goal positions.

    Parameters:
        state (list of lists): The current puzzle state.

    Outputs:
        int: The total Manhattan distance.
    """
    n = len(state)
    total_distance = 0
    goal_positions = {}
    for i in range(n):
        for j in range(n):
            goal_value = i * n + j
            goal_positions[goal_value] = (i, j)

    for i in range(n):
        for j in range(n):
            value = state[i][j]
            if value != 0:
                goal_i, goal_j = goal_positions[value]
                total_distance += abs(i - goal_i) + abs(j - goal_j)
    return total_distance

def h3(state):
    """
    Heuristic function h3: Calculates the Manhattan distance plus linear conflicts.

    Parameters:
        state (list of lists): The current puzzle state.

    Outputs:
        int: The heuristic value (Manhattan distance plus linear conflicts).
    """
    # Calculate the Manhattan distance using h2
    total_distance = h2(state)
    n = len(state)
    linear_conflicts = 0
    
    goal_state = get_goal_state(n)
    
    # Create a mapping from tile value to its goal position
    goal_positions = {}
    for i in range(n):
        for j in range(n):
            value = goal_state[i][j]
            goal_positions[value] = (i, j)
    
    # Detect and count linear conflicts in rows
    for i in range(n):
        current_row = []
        for j in range(n):
            value = state[i][j]
            if value != 0:  # Skip the blank tile
                goal_i, goal_j = goal_positions[value]
                if goal_i == i:  # Tile belongs in the current row
                    current_row.append((value, j))
        # Extract the goal column indices
        goal_columns = [goal_positions[tile[0]][1] for tile in current_row]
        # Count inversions (linear conflicts) within the row
        for m in range(len(goal_columns)):
            for k in range(m + 1, len(goal_columns)):
                if goal_columns[m] > goal_columns[k]:
                    linear_conflicts += 1
    
    # Detect and count linear conflicts in columns
    for j in range(n):
        current_column = []
        for i in range(n):
            value = state[i][j]
            if value != 0:  # Skip the blank tile
                goal_i, goal_j = goal_positions[value]
                if goal_j == j:  # Tile belongs in the current column
                    current_column.append((value, i))
        # Extract the goal row indices
        goal_rows = [goal_positions[tile[0]][0] for tile in current_column]
        # Count inversions (linear conflicts) within the column
        for m in range(len(goal_rows)):
            for k in range(m + 1, len(goal_rows)):
                if goal_rows[m] > goal_rows[k]:
                    linear_conflicts += 1
    
    # Each linear conflict requires two extra moves to resolve
    total_heuristic = total_distance + 2 * linear_conflicts
    return total_heuristic


heuristics = [h1, h2, h3]
def is_solvable(state):
    """
    Determine if the puzzle is solvable when the blank is in the top-left corner.

    Parameters:
        state (list of lists): The initial state of the puzzle.\
        
    Outputs:
        bool: True if the puzzle is solvable, False otherwise.
    """
    n = len(state)
    # Flatten the state into a single list, excluding the blank tile
    flattened_state = [num for row in state for num in row if num != 0]
    inversions = 0
    for i in range(len(flattened_state)):
        current_value = flattened_state[i]
        for j in range(i + 1, len(flattened_state)):
            next_value = flattened_state[j]
            if current_value > next_value:
                inversions += 1
    # Find the row index of the blank tile
    for i in range(n):
        if 0 in state[i]:
            blank_row = i  # Zero-based index from the top
            break
    if n % 2 == 1:
        # Odd grid size: solvable if inversions count is even
        solvable = inversions % 2 == 0
    else:
        # Even grid size: solvable if (inversions + blank_row) % 2 == 0
        solvable = (inversions + blank_row) % 2 == 0
    return solvable
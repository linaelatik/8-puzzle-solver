

class PuzzleNode:
    """
    Class PuzzleNode: Represents a node in the search tree for the n^2-1 puzzle (e.g., 8-puzzle).

    Attributes:
        state (list of lists): The current state of the puzzle board.
        parent (PuzzleNode): The parent node leading to this node.
        action (str): The action taken to reach this state (e.g., 'up', 'down').
        cost (int): The cost to reach this node from the start node (g(n)).
        fval (int): The total estimated cost (f(n) = g(n) + h(n)).
    """
    def __init__(self, state, parent=None, action=None, cost=0, fval=0):
        """
        Initialize a new PuzzleNode.

        Parameters:
            state (list of lists): The puzzle state.
            parent (PuzzleNode): The parent node.
            action (str): The action taken to reach this state.
            cost (int): The cost to reach this node.
            fval (int): The total estimated cost.
        """
        self.state = state      # The puzzle state as a list of lists.
        self.parent = parent    # Reference to the parent PuzzleNode.
        self.action = action    # The action taken to reach this node.
        self.cost = cost        # Cost to reach this node (g(n)).
        self.fval = fval        # Estimated total cost (f(n) = g(n) + h(n)).

    def __eq__(self, other):
        """
        Check if two PuzzleNode instances are equal based on their state.
        """
        return self.state == other.state

    def __lt__(self, other):
        """
        Compare two PuzzleNode instances based on their fval for priority queue ordering.
        """
        return self.fval < other.fval

    def find_blank(self):
        """
        Find the position of the blank (0) in the puzzle.

        Returns:
            tuple: Coordinates (i, j) of the blank tile.
        """
        n = len(self.state)
        for i in range(n):
            for j in range(n):
                if self.state[i][j] == 0:
                    return i, j
        return None  # Should never happen if blank is always present.

    def generate_successors(self):
        """
        Generate child nodes by moving the blank tile in all possible directions.

        Returns:
            list: A list of successor PuzzleNode instances.
        """
        successors = []
        n = len(self.state)
        x, y = self.find_blank()
        # Possible moves: up, down, left, right
        moves = [(-1, 0, 'up'), (1, 0, 'down'), (0, -1, 'left'), (0, 1, 'right')]
        for dx, dy, action in moves:
            x_new, y_new = x + dx, y + dy
            if 0 <= x_new < n and 0 <= y_new < n:
                # Create a deep copy of the state
                new_state = [row[:] for row in self.state]
                # Swap the blank with the adjacent tile
                new_state[x][y], new_state[x_new][y_new] = new_state[x_new][y_new], new_state[x][y]
                # Create a new PuzzleNode for the successor
                child_node = PuzzleNode(new_state, parent=self, action=action, cost=self.cost + 1)
                successors.append(child_node)
        return successors

    def __str__(self):
        """
        Return a string representation of the puzzle state as a grid.

        Returns:
            str: The grid representation of the state.
        """
        return '\n'.join(['\t'.join(map(str, row)) for row in self.state])
    
    @staticmethod
    def is_goal(state, goal_state):
        """
        Check if the current state is the goal state.

        Parameters:
            state (list of lists): The puzzle state to check.

        Returns:
            bool: True if the state is the goal state, False otherwise.
        """
        #n = len(state)
        return state == goal_state
    
    
def get_goal_state(n, as_tuple=False):
    """
    Generate the goal state for an n x n puzzle.

    Parameters:
        n (int): The dimension of the puzzle.
        as_tuple (bool): Whether to return the state as a tuple of tuples.

    Returns:
        list of lists or tuple of tuples: The goal state.
    """
    goal_state = [[i * n + j for j in range(n)] for i in range(n)]
    if as_tuple:
        return tuple(tuple(row) for row in goal_state)
    return goal_state
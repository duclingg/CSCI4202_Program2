import random
import sys
import json

sys.stderr.write("Connect Four - Python\n")

# Extract command line arguments
player = int(sys.argv[2])  # --player <p>
width = int(sys.argv[4])   # --width <w>
height = int(sys.argv[6])  # --height <h>

sys.stderr.write("player = " + str(player) + '\n')
sys.stderr.write("width = " + str(width) + '\n')
sys.stderr.write("height = " + str(height) + '\n')

def valid_moves(state):
    """Returns the valid moves for the state as a list of integers."""
    """
        takes the JSON format as input for the game state
        extracts a 2d 'grid' from the passed object 'state'
        This function is called by "best_move" to get a list of valid column "places" to put the "piece"
    """
    grid = state['grid']
    moves = []
    """
        loops through each column of the passed object (state) and checks if a move can be made to
        the column.
        columns are valid if nothing is in the top cell of the row
    """
    for i in range(width):
        if grid[i][0] == 0:
            moves.append(i)
    return moves  # returns list of valid locations to move

# def apply_move(grid, col, player):
#     """Simulates applying a move to the board and returns a new grid."""
#     new_grid = [row[:] for row in grid]  # Deep copy the grid
#     """
#         finds the first empty row, from the bottom, and places the a "piece" in that row
#         This function only simulates moves, and is not actually used, and is a simulation
#     """
#     for row in reversed(new_grid):
#         if row[col] == 0:  # Find the first empty row from the bottom
#             row[col] = player
#             break
#     return new_grid

def best_move(state):
    """Returns the best move by randomly choosing from valid moves (for now)."""
    """
        Used to choose a random move, from the list returned by the function 'valid moves'
    """
    valid_moves_list = valid_moves(state)
    return random.choice(valid_moves_list)  # Simple random selection for now

# Loop to read the state from the Lisp driver and output the move
for line in sys.stdin:
        sys.stderr.write(line)
        state = json.loads(line)
        # Choose the best move based on the current game state
        action = {'move': best_move(state)}
        msg = json.dumps(action)
        sys.stderr.write(msg + '\n')
        sys.stdout.write(msg + '\n')
        sys.stdout.flush()

# Be a nice program and close the ports
sys.stdin.close()
sys.stdout.close()
sys.stderr.close()

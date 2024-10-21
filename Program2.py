import sys
import json
import math

sys.stderr.write("Connect Four - Python with Alpha-Beta Pruning\n")

player = int(sys.argv[2])
width = int(sys.argv[4])
height = int(sys.argv[6])

sys.stderr.write(f"player = {player}\n")
sys.stderr.write(f" width = {width}\n")
sys.stderr.write(f"height = {height}\n")

def valid_moves(grid):
    return [col for col in range(width) if grid[col][0] == 0]

def make_move(grid, col, player):
    new_grid = [column[:] for column in grid]
    for row in range(height - 1, -1, -1):
        if new_grid[col][row] == 0:
            new_grid[col][row] = player
            return new_grid
    return None

def check_winner(grid, player):
    # Check horizontal
    for row in range(height):
        for col in range(width - 3):
            if all(grid[col+i][row] == player for i in range(4)):
                return True
    
    # Check vertical
    for col in range(width):
        for row in range(height - 3):
            if all(grid[col][row+i] == player for i in range(4)):
                return True
    
    # Check diagonal (positive slope)
    for col in range(width - 3):
        for row in range(height - 3):
            if all(grid[col+i][row+i] == player for i in range(4)):
                return True
    
    # Check diagonal (negative slope)
    for col in range(width - 3):
        for row in range(3, height):
            if all(grid[col+i][row-i] == player for i in range(4)):
                return True
    
    return False

def evaluate_position(grid):
    if check_winner(grid, player):
        return 1000
    elif check_winner(grid, 3 - player):
        return -1000
    else:
        return 0

def alpha_beta(grid, depth, alpha, beta, maximizing_player):
    valid_moves_list = valid_moves(grid)
    if depth == 0 or not valid_moves_list:
        return evaluate_position(grid)
    
    if maximizing_player:
        value = -math.inf
        for move in valid_moves_list:
            new_grid = make_move(grid, move, player)
            value = max(value, alpha_beta(new_grid, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = math.inf
        for move in valid_moves_list:
            new_grid = make_move(grid, move, 3 - player)
            value = min(value, alpha_beta(new_grid, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

def best_move(grid):
    best_score = -math.inf
    best_move = None
    for move in valid_moves(grid):
        new_grid = make_move(grid, move, player)
        score = alpha_beta(new_grid, 5, -math.inf, math.inf, False)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

for line in sys.stdin:
    sys.stderr.write(line)
    state = json.loads(line)
    action = {"move": best_move(state['grid'])}
    msg = json.dumps(action)
    sys.stderr.write(msg + '\n')
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()

sys.stdin.close()
sys.stdout.close()
sys.stderr.close()
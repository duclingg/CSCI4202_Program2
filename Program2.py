import sys
import json
import random

player = int(sys.argv[2])
width = int(sys.argv[4])
height = int(sys.argv[6])

sys.stderr.write(f"player = {player}\n")
sys.stderr.write(f" width = {width}\n")
sys.stderr.write(f"height = {height}\n")

opponent = 3 - player

def valid_moves(grid):
    return [col for col in range(width) if grid[col][0] == 0]

def drop_piece(grid, col, piece):
    for row in range(height-1, -1, -1):
        if grid[col][row] == 0:
            return row
    return -1

def check_winner(grid, col, row, piece):
    # Check horizontal
    count = 0
    for c in range(max(0, col-3), min(width, col+4)):
        if grid[c][row] == piece:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    if row <= height - 4:
        if all(grid[col][row+i] == piece for i in range(4)):
            return True
    
    # Check diagonal (positive slope)
    count = 0
    for i in range(-3, 4):
        if 0 <= col+i < width and 0 <= row+i < height:
            if grid[col+i][row+i] == piece:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    
    # Check diagonal (negative slope)
    count = 0
    for i in range(-3, 4):
        if 0 <= col+i < width and 0 <= row-i < height:
            if grid[col+i][row-i] == piece:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    
    return False

def evaluate_position(grid):
    score = 0
    for col in range(width):
        for row in range(height):
            if grid[col][row] == player:
                score += col + 1  # Prefer center columns
            elif grid[col][row] == opponent:
                score -= col + 1
    return score

def alpha_beta(grid, depth, alpha, beta, maximizing_player):
    valid_moves_list = valid_moves(grid)
    if depth == 0 or not valid_moves_list:
        return evaluate_position(grid)
    
    if maximizing_player:
        value = float('-inf')
        for move in valid_moves_list:
            row = drop_piece(grid, move, player)
            grid[move][row] = player
            if check_winner(grid, move, row, player):
                grid[move][row] = 0
                return float('inf')
            value = max(value, alpha_beta(grid, depth - 1, alpha, beta, False))
            grid[move][row] = 0
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for move in valid_moves_list:
            row = drop_piece(grid, move, opponent)
            grid[move][row] = opponent
            if check_winner(grid, move, row, opponent):
                grid[move][row] = 0
                return float('-inf')
            value = min(value, alpha_beta(grid, depth - 1, alpha, beta, True))
            grid[move][row] = 0
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

def best_move(grid):
    valid_moves_list = valid_moves(grid)
    best_score = float('-inf')
    best_moves = []
    
    for move in valid_moves_list:
        row = drop_piece(grid, move, player)
        grid[move][row] = player
        
        if check_winner(grid, move, row, player):
            grid[move][row] = 0
            return move
        
        score = alpha_beta(grid, 5, float('-inf'), float('inf'), False)
        grid[move][row] = 0
        
        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)
    
    return random.choice(best_moves)

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
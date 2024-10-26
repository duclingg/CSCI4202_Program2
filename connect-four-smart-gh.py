# Connect 4 Bot 
#
# Author: Garrett Hoiness
#
# Running as of : 10/24/24
#
#

import random
import sys
import json

sys.stderr.write("Connect Four - Python - Smart\n")

# This is fragile and relies on the fact that the driver always passes the
# command line arguments in the order --player <p> --width <w> --height <h>.
player = int(sys.argv[2]) # --player <p>

# set constant player and opp values
"""oppchip = 0
playchip = player 
if (player == 1):
	oppchip = 2
else:
	oppchip = 1"""

width = int(sys.argv[4]) # --width <w>
height = int(sys.argv[6]) # --height <h>

sys.stderr.write("player = " + str(player) + '\n')
sys.stderr.write("width = " + str(width) + '\n')
sys.stderr.write("height = " + str(height) + '\n')

def valid_moves(state):
    """Returns the valid moves for the state as a list of integers."""
    grid = state['grid']
    moves = []
    for i in range(width):
        if grid[i][0] == 0:
            moves.append(i)
    return moves

# gets the next free row to drop a piece into
def get_row(state,column,height):
	gridstate = state['grid']

	for i in range(height-1,-1,-1):
		
		if i == 0 and gridstate[column][i+1] > 0:
			return i
		# solve edge case
		if gridstate[column][i] == 0 and gridstate[column][i-1] == 0:
			return i

# checks if the game is in a terminal state (no more moves left or a win for the player)
def terminal_check(grid, movelist):
	return win_check(grid,player) or len(movelist) == 0

# checks if there is a winning pattern for the player, returns True if yes, False if not
def win_check(grid,piece):

	# check for horizontal win
	for col in range(width-3):
		for row in range(height):
			if grid[col][row] == piece and grid[col+1][row] == piece and grid[col+2][row] == piece and grid[col+3][row] == piece:
				return True

	# check for vertical win
	for col in range(width):
		for row in range(height-3):
			if grid[col][row] == piece and grid[col][row+1] == piece and grid[col][row+2] == piece and grid[col][row+3] == piece:
				return True

	# check for diagonal up win
	for col in range(width-3):
		for row in range(height-3):
			if grid[col][row] == piece and grid[col+1][row+1] == piece and grid[col+2][row+2] == piece and grid[col+3][row+3] == piece:
				return True

	# check for diagonal down win
	for col in range(width-3):
		for row in range(3, height):
			if grid[col][row] == piece and grid[col+1][row-1] == piece and grid[col+2][row-2] == piece and grid[col+3][row-3] == piece:
				return True

# gathers the pieces placed by the player and submits the values to an eval function to be scored
def score_position(grid, player):

	# initialize score
    score = 0

    # score center
    centerarr = []
    centercol = int(width/2)
    for row in range(height):
    	centerarr.append(int(grid[centercol][row]))
    centercount = centerarr.count(player)
    score += centercount * 3



    # score horizontals
    for row in range(height):
    	rowarr = []
    	for col in range(width):
    		chip = grid[col][row]
    		rowarr.append(int(chip))

    	for col in range(width-3):
    		scorewindow = rowarr[col:col+4]
    		score += eval_score(scorewindow, player)

    # score verticals
    for col in range(width):
    	colarr = []
    	for chip in grid[col]:
    		colarr.append(int(chip))

    	for row in range(height-3):
    		scorewindow = colarr[row:row + 4]
    		score += eval_score(scorewindow,player)

    # score diagonals up
    for col in range(width-3):
    	for row in range(height-3):
    		scorewindow = [grid[col+i][row+i] for i in range(4)]
    		score += eval_score(scorewindow,player)

    # score diagonals down
    for col in range(width-3):
    	for row in range(height-3):
    		scorewindow = [grid[col+3-i][row+i] for i in range(4)]
    		score += eval_score(scorewindow,player)
    return score

# returns a sum based on the amount of chips placed by the player in question.
# scores are weighted on winning, 3 in a row, 2 in a row, and the possibility to 
# block the opponent 
def eval_score(window,player):
	score = 0
	oppchip = player
	if player == oppchip:
		oppchip = 2

	# tally winning score
	if window.count(player) == 4:
		score += 100

	# tally 3 in a row
	elif window.count(player) == 3 and window.count(0) == 1:
		score += 5

	# tally 2 in a row
	elif window.count(player) == 2 and window.count(0) == 2:
		score ++ 2

	# tally blocking opp
	if window.count(oppchip) == 3 and window.count(0) == 1:
		score -= 4

	return score

# tries moves to find the best move
def alphabeta(state,depth,alpha, beta, height, maximizePlayer):

	# establish valid move list
	movelist = valid_moves(state)
	grid = state['grid']
	terminal = terminal_check(grid, movelist)

	# if its maxed out or a win, return that
	if depth == 0 or terminal:
		if terminal:

			# if player wins
			if win_check(grid,1):
				return None,999999

			# if board is full
			if len(movelist) == 0:
				return None,0
		else:
			return None, score_position(grid,player)

	# if its the maximizing players turn, choose the best move possible
	# to maximize the score value
	if maximizePlayer:
		value = -99999999
		bestcol = None

		# for each column in the valid moves, try a move
		for col in movelist:
			row = get_row(state,col,height)
			statecopy = state.copy()
			
			statecopy['grid'][col][row] = player
			gridcopy = statecopy['grid']

			_, newscore = alphabeta(statecopy,depth-1,alpha,beta,height,False)
			
			# if the newscore is greater than the original value, replace it and
			# choose that column as the new best maximizing move
			if newscore > value:
				value = newscore
				bestcol = col
				
			alpha = max(alpha,value)
			if alpha >= beta:
				break
		return bestcol,value

	# if its the minimizing players turn, choose the best move possible
	# to minimize the score value
	else:
		value = 999999
		bestcol = None

		# for each column in the valid moves, try a move
		for col in movelist:
			row = get_row(state,col,height)
			statecopy = state.copy()
			
			statecopy['grid'][col][row] = 2
			gridcopy = statecopy['grid']
			
			_, newscore = alphabeta(statecopy,depth-1,alpha,beta,height,True)
			
			# if the newscore is less than the original value, replace it and
			# choose that column as the new best minimizing move
			if newscore < value:
				value = newscore
				bestcol = col

			beta = min(beta,value)
			if alpha >= beta:
				break
		return bestcol,value

# driver for assessing best move for the player, passing to the alphabeta
# function and then when a move has been found, returning it 
def best_move(state,depth,height):
	finalcol, _ = alphabeta(state,depth,float('-inf'), float('+inf'), height, True)
	return finalcol

# Prints out a much easier to read grid state of the board
# to std-err (used in debugging)
def grid_print(gridstate):
	
	k = 0
	while k < height:
		for i in range(width):
			sys.stderr.write(str(gridstate[i][k]) + ' ')
		sys.stderr.write('\n')
		k += 1
##
##
## main loop ##
##
##
# Loop reading the state from the driver and writing a random valid move.
for line in sys.stdin:

	# load state
    state = json.loads(line)

    # put state into list of columns
    gridstate = state['grid']

    # print human readable board state (for debugging)
    #grid_print(gridstate)

    # current depth is 42 moves ahead
    bestmove = best_move(state,42,height)
    sys.stderr.write("Best move chosen is " + str(bestmove) + "\n")
    action = {}
    action['move'] = bestmove
    msg = json.dumps(action)

    # write to stderr file
    sys.stderr.write(msg + '\n')

    # write to driver
    sys.stdout.write(msg + '\n')

    # flush stdout
    sys.stdout.flush()

# Be a nice program and close the ports.
sys.stdin.close()
sys.stdout.close()
sys.stderr.close()
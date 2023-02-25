# MATH 381 Assignment 6
# Xinghan Guo
# Simulation game - "Occupation"
import numpy as np
import random

numberOfGames = 10000
numberOfRuns = 10
min_prob = 100
max_prob = -100

# In the matrix:
# A - 1
# B - 2
# Common - 0.5
# Empty - 0

for run in range(numberOfRuns):
    A_wins = 0
    B_wins = 0
    for game in range(numberOfGames+1):

        board = np.zeros((5,5)) # 5 x 5 board
        numofA = 1
        numofB = 1

        i = list(range(0,5))
        j = list(range(0,5))
        random.shuffle(i)
        random.shuffle(j)
        current_position_A = [i[0], j[0]]
        ai = current_position_A[0]  # Random starting position for A
        aj = current_position_A[1]  # Random starting position for A

        current_position_B = [i[1], j[1]]
        bi = current_position_B[0]  # Random starting position for B
        bj = current_position_B[1]  # Random starting position for B

        board[ai, aj] = 1 # value for A
        board[bi, bj] = 2 # value for B
        #print([ai,aj])
        #print([bi,bj])

        maximum_numofPlays = 10 # 10 rounds for each game
        numofPlays = 0 # record the number of games
        while(numofPlays < maximum_numofPlays):
            # record A's and B's adjacents positions and values (left, right, up, down)
            A_adjacents = {0: [], 2: [], 1: [], 0.5: []}
            B_adjacents = {0: [], 2: [], 1: [], 0.5: []}

            # discover adjecent four boxes around current A
            if ai+1 in range(5): # can not exceed the frontier
                A_adjacents[board[ai+1, aj]] += [[ai+1, aj]] # down
            if ai-1 in range(5):
                A_adjacents[board[ai-1, aj]] += [[ai-1, aj]] # up
            if aj+1 in range(5):
                A_adjacents[board[ai, aj+1]] += [[ai, aj+1]] # right
            if aj-1 in range(5):
                A_adjacents[board[ai, aj-1]] += [[ai, aj-1]] # left
            #print(A_adjacents)

            # discover adjecent four boxes around current B
            if bi+1 in range(5):
                B_adjacents[board[bi+1, bj]] += [[bi+1, bj]] # down
            if bi-1 in range(5):
                B_adjacents[board[bi-1, bj]] += [[bi-1, bj]] # up
            if bj+1 in range(5):
                B_adjacents[board[bi, bj+1]] += [[bi, bj+1]] # right
            if bj-1 in range(5):
                B_adjacents[board[bi, bj-1]] += [[bi, bj-1]] # left
            #print(B_adjacents)

            ### A's strategy
            next_step_A = [] # best choices for A (may have TIE!)
            if numofA - numofB > 6: # may change due to different strategies
                # prefer empty > B > A > common
                if A_adjacents[0] != []:
                    next_step_A = A_adjacents[0]
                elif A_adjacents[2] != []:
                    next_step_A = A_adjacents[2]
                elif A_adjacents[1] != []:
                    next_step_A = A_adjacents[1]
                elif A_adjacents[0.5] != []:
                    next_step_A = A_adjacents[0.5]
            else:
                # prefer B > empty > A > common
                if A_adjacents[2] != []:
                    next_step_A = A_adjacents[2]
                elif A_adjacents[0] != []:
                    next_step_A = A_adjacents[0]
                elif A_adjacents[1] != []:
                    next_step_A = A_adjacents[1]
                elif A_adjacents[0.5] != []:
                    next_step_A = A_adjacents[0.5]
            #print(next_step_A)
            random.shuffle(next_step_A) # in case of tie, randomly choose one
            #print(next_step_A)

            # next position for A
            A_move_to_position = [next_step_A[0][0], next_step_A[0][1]]
            # current status of A's next position
            A_move_to_value = board[next_step_A[0][0], next_step_A[0][1]]
            #print(A_move_to_position)
            #print(A_move_to_value)


            ### B's strategy
            next_step_B = [] # best choices for B (may have TIE!)
            if numofB - numofA > 6: # may change due to different strategies
                # prefer empty > A > B > common
                if B_adjacents[0] != []:
                    next_step_B = B_adjacents[0]
                elif B_adjacents[1] != []:
                    next_step_B = B_adjacents[1]
                elif B_adjacents[2] != []:
                    next_step_B = B_adjacents[2]
                elif B_adjacents[0.5] != []:
                    next_step_B = B_adjacents[0.5]
            else:
                # prefer A > empty > B > common
                if B_adjacents[1] != []:
                    next_step_B = B_adjacents[1]
                elif B_adjacents[0] != []:
                    next_step_B = B_adjacents[0]
                elif B_adjacents[2] != []:
                    next_step_B = B_adjacents[2]
                elif B_adjacents[0.5] != []:
                    next_step_B = B_adjacents[0.5]
            #print(next_step_B)
            random.shuffle(next_step_B) # in case of tie, randomly choose one
            #print(next_step_B)
            # next position for B
            B_move_to_position = [next_step_B[0][0], next_step_B[0][1]]
            # current status of B's next position
            B_move_to_value = board[next_step_B[0][0], next_step_B[0][1]]
            #print(B_move_to_position)
            #print(B_move_to_value)

            #print(np.array_equal(A_move_to_position, B_move_to_position))

            # if A and B didn't meet at the next position
            #   for A:
            #       next position is empty - belong A - numofA+1 - value = 1
            #       next position is B's - belong A - numofA+1 & numofB-1 - value =1
            #   for B:
            #       next position is empty - belong B - numofB+1 - value=2
            #       next position is A's - belong B - numofB+1 & numofA-1 - value=2
            #
            # if A and B meet at the next position
            #       new position=0.5
            #       next position is empty - common - numofA+0.5 & numofB+0.5
            #       next position is A's - common - numofA-0.5 & numofB+0.5
            #       next position is B's - common - numofB-0.5 & numofA+0.5
            #
            if np.array_equal(A_move_to_position, B_move_to_position) == False:
                if A_move_to_value == 0:
                    board[A_move_to_position[0], A_move_to_position[1]] = 1
                    numofA += 1
                elif A_move_to_value == 2:
                    board[A_move_to_position[0], A_move_to_position[1]] = 1
                    numofA += 1
                    numofB -= 1

            if np.array_equal(A_move_to_position, B_move_to_position) == False:
                if B_move_to_value == 0:
                    board[B_move_to_position[0], B_move_to_position[1]] = 2
                    numofB += 1
                elif B_move_to_value == 1:
                    board[B_move_to_position[0], B_move_to_position[1]] = 2
                    numofA -= 1
                    numofB += 1

            if np.array_equal(A_move_to_position, B_move_to_position) == True:
                board[A_move_to_position[0], A_move_to_position[1]] = 0.5
                if A_move_to_value == 1:
                    numofA = numofA - 0.5
                    numofB = numofB + 0.5
                elif A_move_to_value == 2:
                    numofA = numofA + 0.5
                    numofB = numofB - 0.5
                elif A_move_to_value == 0:
                    numofA = numofA + 0.5
                    numofB = numofB + 0.5

            # update current positions Of A and B
            current_position_A = A_move_to_position
            current_position_B = B_move_to_position
            ai = current_position_A[0]
            aj = current_position_A[1]
            bi = current_position_B[0]
            bj = current_position_B[1]

            numofPlays += 1
            #print(current_position_A)
            #print(current_position_B)
            #print(numofA)
            #print(numofB)

        # WINNER!!
        if numofA > numofB:
            A_wins += 1
        elif numofA < numofB:
            B_wins += 1
        else:
            A_wins += 1
            B_wins += 1
        #print(numofPlays)
        #print(numofA)
        #print(numofB)

        # for each run, numer of games has been run and averaging the probability
        #if ((game % 20 == 0) and (game > 0)):
            #print(run)
            #print(game)
            #print(A_wins * 1./game)

    # Winning probability of A&B after each run ends (10runs - 10probabilities)
    probablity_A_wins = A_wins * 1./ numberOfGames
    #probablity_B_wins = B_wins * 1./ numberOfGames
    #print(run)
    #print(game)
    #print(probablity_A_wins)

    # calculate the min & max winning probability
    if probablity_A_wins < min_prob:
        min_prob = probablity_A_wins

    if probablity_A_wins > max_prob:
        max_prob = probablity_A_wins
    #print(run, ' ', probablity_B_wins)
print(min_prob, ' ', max_prob)


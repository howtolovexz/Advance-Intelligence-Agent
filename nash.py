# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 23:36:27 2018

@author: JaZz-
"""

import numpy as np
from collections import Counter

##############################################################################

def get_dominant_strategy(payoff_matrix):
    shape = payoff_matrix.shape
    
    # find index for maximum payoff
    winner_index_list = np.argwhere(payoff_matrix == np.amax(payoff_matrix, axis = 0))
    
    # create list of row index
    row_index_list = []
    for i in range(winner_index_list.shape[0]):
        row_index_list.append(winner_index_list[i][0])
        
    # count each row index
    row_count_array = Counter(row_index_list)
    
    # compare count with size of column (another player payoff)
    dominant_strategy_flag = 0
    dominant_strategy_list = []
    for i in range(0, shape[0]):
        if(row_count_array[i] == shape[1]):
            dominant_strategy_flag = 1
            dominant_strategy_list.append(i + 1)
            #print("Dominant Strategy is strategy: " + str(i + 1))
        
    return dominant_strategy_list, dominant_strategy_flag



def get_nash(payoff1, payoff2):
    shape = payoff1.shape
    # create matrix to store count of being nash equilibrium/equilibria
    w, h = shape[1], shape[0];
    nash_matrix = [[0 for x in range(w)] for y in range(h)]
    
    # find max payoff for player 1 if fixed player 2 strategy
    winner_index_list = np.argwhere(payoff1 == np.amax(payoff1, axis = 0))
    for winner_index in winner_index_list:
        nash_matrix[winner_index[0]][winner_index[1]] += 1
        
    # find max payoff for player 2 if fixed player 1 strategy
    winner_index_list = np.argwhere(payoff2 == np.amax(payoff2, axis = 1))
    for winner_index in winner_index_list:
        nash_matrix[winner_index[0]][winner_index[1]] += 1
    
    # check count in each strategy if equal to 2 means it is a pure Nash
    pure_nash_list = []
    for i in range(0, h):
        for j in range(0, w):
            if(nash_matrix[i][j] == 2):
                pure_nash_list.append([i + 1, j + 1])

    return pure_nash_list


# =============================================================================
# def get_mixed_nash(payoff):
#     row = payoff.shape[0]
#     col = payoff.shape[1]
#     
#     coefficient_list = [[0 for x in range(col - 1)] for y in range(row - 1)]
#     constant_list = [0 for y in range(row - 1)]
#     
#     # calculate coefficient for each strategy of Player 1 from expected utillity for each strategy of Player 2
#     # eg. E(Left) = E(Right)
#     # p1 = coefficient from strategy L minus R and the last strategy (1 - p1 - p2)
#     for i in range(0, col - 1):
#         for j in range(0, row - 1):
#             coe = payoff[i, j] - payoff[row - 1, j] - payoff[i, j + 1] + payoff[row - 1, j + 1]
#             coefficient_list[j][i] = coe
#         con = payoff[col - 1, i + 1] - payoff[col - 1, i] 
#         constant_list[i] = con
#     
#     coefficient_list = np.array(coefficient_list)
#     constant_list = np.array(constant_list)
#     prob_list = np.linalg.solve(coefficient_list, constant_list)
#     last_prob = 1
#     for prob in prob_list:
#         last_prob -= prob
#     
#     last_prob = np.array([last_prob])
#     prob_list = np.append(prob_list, last_prob)
#     print("Probability for Player 1")
#     print(prob_list)
# =============================================================================
    
# =============================================================================
# def get_mixed_nash(payoff):
#     row = payoff.shape[0]
#     col = payoff.shape[1]
#     
#     coefficient_list = [[0 for x in range(1)] for y in range(1)]
#     constant_list = [0 for y in range(1)]
#     
#     print(coefficient_list)
#     print(constant_list)
#     
#     # calculate coefficient for each strategy of Player 1 from expected utillity for each strategy of Player 2
#     # eg. E(Left) = E(Right)
#     # p1 = coefficient from strategy L minus R and the last strategy (1 - p1 - p2)
#     for i in range(0, 1):
#         for j in range(0, 1):
#             coe = payoff[i, j] - payoff[1, j] - payoff[i, j + 1] + payoff[1, j + 1]
#             coefficient_list[j][i] = coe
#         con = payoff[1, i + 1] - payoff[1, i] 
#         constant_list[i] = con
#     
#     coefficient_list = np.array(coefficient_list)
#     constant_list = np.array(constant_list)
#     prob_list = np.linalg.solve(coefficient_list, constant_list)
#     last_prob = 1
#     for prob in prob_list:
#         last_prob -= prob
#     
#     last_prob = np.array([last_prob])
#     prob_list = np.append(prob_list, last_prob)
#     print("Probability for Player 1")
#     print(prob_list)
# =============================================================================
    
    
def get_mixed_nash(payoff):
    row = payoff.shape[0]
    col = payoff.shape[1]
    
    strategy_list = [y + 1 for y in range(row)]
    coefficient_list = [[0 for x in range(col - 1)] for y in range(row - 1)]
    constant_list = [0 for y in range(row - 1)]
    
    # calculate coefficient for each strategy of Player 1 from expected utillity for each strategy of Player 2
    # eg. E(Left) = E(Right)
    # p1 = coefficient from strategy L minus R and the last strategy (1 - p1 - p2)
    for i in range(0, col - 1):
        for j in range(0, row - 1):
            coe = payoff[i, j] - payoff[row - 1, j] - payoff[i, j + 1] + payoff[row - 1, j + 1]
            coefficient_list[j][i] = coe
        con = payoff[col - 1, i + 1] - payoff[col - 1, i] 
        constant_list[i] = con
    
    if(np.linalg.det(coefficient_list) == 0):
        print("Cannot find mixed Nash")
        return [], []
        
    coefficient_list = np.array(coefficient_list)
    constant_list = np.array(constant_list)
    prob_list = np.linalg.solve(coefficient_list, constant_list)
    
    last_prob = 1
    for prob in prob_list:
        last_prob -= prob
    
    last_prob = np.array([last_prob])
    prob_list = np.append(prob_list, last_prob)
    
    # check for negative probability remove those strategies
    count = 0
    negative_prob_flag = 0
    for prob in prob_list:
        if(prob < 0):
            payoff = np.delete(payoff, [count], axis=0)
            payoff = np.delete(payoff, [col - 1], axis=1)
            strategy_list.remove(count + 1)
            prob_list[count] = 0
            negative_prob_flag = 1
        count += 1
    
    # if there are some negative probability recalculate probability without those strategies
    if(negative_prob_flag == 1):
        prob_list_new, strategy_list_new = get_mixed_nash(payoff)
        prob_list = prob_list_new
        
    return prob_list, strategy_list
    
##############################################################################
# get input payoff matrix
# =============================================================================
# row_count = int(input("Number of Row Player Strategy: "))
# col_count = int(input("Number of Column Player Strategy: "))
# 
# payoff = []
# for i in range(0, row_count):
#     temp = input("Strategy " + str(i + 1) + " Payoff for Player 1: ").split()
#     temp = list(map(int, temp))
#     payoff.append(temp)
#     
# payoff1 = np.matrix(payoff)
# 
# payoff = []
# for i in range(0, row_count):
#     temp = input("Strategy " + str(i + 1) + " Payoff for Player 2: ").split()
#     temp = list(map(int, temp))
#     payoff.append(temp)
#     
# payoff2 = np.matrix(payoff)
# =============================================================================
##############################################################################
    

############################## Input Matrix ##################################
random_list = np.random.randint(3, size=(3, 3))
payoff1 = np.matrix(random_list)
random_list = np.random.randint(3, size=(3, 3))
payoff2 = np.matrix(random_list)
payoff2 = np.matrix("2 6 4; 12 3 5; 6 0 2")
#payoff2 = np.matrix("0 3 4 5 6; 3 0 5 6 7; 4 5 0 7 8; 5 6 7 0 9; 6 7 8 9 0")
#payoff2 = np.matrix("3 0 5 6; 4 5 0 7; 5 6 7 0; 6 7 8 9")
payoff1 = np.matrix("5 5 3 3; 5 5 2 2; 4 4 4 4; 4 1 4 1")
payoff2 = np.matrix("5 5 2 2; 5 5 3 3; 3 0 3 0; 3 2 3 2")
##############################################################################


########################### Dominant Strategy ################################
print("Dominant strategy")
print("Player 1")
dominant_strategy_list, dominant_strategy_flag = get_dominant_strategy(payoff1)
if(dominant_strategy_flag == 0):
    print("No Dominant Strategy for this player")
else:
    print("Dominant Strategy is/are strategy: ")
print(*dominant_strategy_list)
print("Player 2")
dominant_strategy_list, dominant_strategy_flag = get_dominant_strategy(payoff2)
if(dominant_strategy_flag == 0):
    print("No Dominant Strategy for this player")
else:
    print("Dominant Strategy is/are strategy: ")
print(*dominant_strategy_list)
print()
##############################################################################

########################## Pure Nash Equilibrium #############################
print("Nash equilibrium/equilibria: ")
print(get_nash(payoff1, payoff2))
print()
##############################################################################

######################### Mixed Nash Equilibrium #############################
prob_list, strategy_list = get_mixed_nash(payoff2)
print("Mixed Nash Equilibrium strategies for Player 1: " + str(strategy_list))
print("with probability: " + str(prob_list))
##############################################################################
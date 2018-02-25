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
            
    if(dominant_strategy_flag == 0):
        print("No Dominant Strategy for this player")
    else:
        print("Dominant Strategy is/are strategy: ")
        print(*dominant_strategy_list)


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
    
    nash_count = 2
    print("Nash equilibrium/equilibria: ")
    print([(index, row.index(nash_count)) for index, row in enumerate(nash_matrix) if nash_count in row])
    
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
payoff1 = np.matrix("3 2 2; 3 1 5")
payoff2 = np.matrix("3 3 4; 1 3 0")
##############################################################################

print("Player 1")
get_dominant_strategy(payoff1)
print()
print("Player 2")
get_dominant_strategy(payoff2)
print()

get_nash(payoff1, payoff2)
print()
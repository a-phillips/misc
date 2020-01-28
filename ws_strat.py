#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 17:11:07 2020

@author: aphillips

Implementation of algorithm from GS interview.

Problem: You would like to bet on a team to win the world series with even odds.
The world series is won when either team reaches 4 wins, also called best of 7.
The bookie is only willing to allow bets on individual games. All individual games
have even odds. What strategy do you use to determine the apprpriate bets to make
to replicate your desired entire-series bet?

Solution: We are looking to force our "wealth" to +1 if the desired team wins and
-1 if the desired team loses. We can imagine these as the terminal wealth values
of a binomial tree, which ends whenever either team reaches 4 wins. With even odds,
our wealth at a current (win, loss) node must be the average of wealth after 1 more win
or one more loss, since wealth after a win is wealth + bet, and wealth after a loss is
wealth - bet. We can recursively determine those future wealth values, or walk back
in the tree starting at the (3 wins, 3 losses) node. The below code implements both.
"""



import numpy as np

def run_recursive(first_to):
    
    # Define recursive wealth function as the average of the wealth at the two
    # future (win, loss) nodes, with the conditions that wealth = 1 if the series
    # is won and wealth = -1 if the series is lost
    def wealth(wins, losses):
        if wins == first_to:
            return 1.0
        elif losses == first_to:
            return -1.0
        else:
            return (wealth(wins + 1, losses) + wealth(wins, losses + 1)) / 2
    
    
    wealth_grid = np.zeros((first_to + 1, first_to + 1))
    bet_grid = np.zeros((first_to + 1, first_to + 1))
    
    # Populate the wealth grid using the recursive function
    for wins in range(first_to + 1):
        for losses in range(first_to + 1):
            wealth_grid[wins, losses] = wealth(wins, losses)
    
    # Calculate eh bet size as the winning node wealth less the current node wealth 
    for wins in range(first_to):
        bet_grid[wins] = wealth_grid[wins+1] - wealth_grid[wins]
    
    # Display the results
    print('Wealth:')
    print(wealth_grid.round(4))
    print('Bets:')
    print(bet_grid.round(4))
    print('-'*80)

def run_iterative(first_to):

    # Calculate max number of games and initiate wealth and bet matrices
    # Note wealth[x, y] means your team has won x games, opposing team has won y
    max_games = (2 * first_to) - 1
    
    wealth = np.zeros((first_to + 1, first_to + 1))
    bet = np.zeros((first_to + 1, first_to + 1))

    # Set values at terminal nodes
    for losses in range(first_to):
        wealth[first_to, losses] = 1
        wealth[losses, first_to] = -1
    
    # Loop backward based on total number of games played
    for num_games in range(max_games - 1, -1, -1):
        
        # Loop through possible win/loss combos
        for wins in range(min(first_to, num_games+1)):
            losses = num_games - wins
            # Losses must be less than total required winning games to be valid
            if losses < first_to:
                
                # Wealth at current node needs to be average of wealth at next future nodes
                wealth_win = wealth[wins + 1, losses]
                wealth_loss = wealth[wins, losses + 1]
                curr_wealth_target = (wealth_win + wealth_loss) / 2
                wealth[wins, losses] = curr_wealth_target
                
                # Bet size is therefore the difference between wealth at winning node and current node
                bet[wins, losses] = wealth_win - curr_wealth_target
    
    # Display the results
    print('Wealth:')
    print(wealth.round(4))
    print('Bets:')
    print(bet.round(4))
    print('-'*80)



if __name__ == '__main__':
    print('Iterative:')
    run_iterative(4)
    print('Recursive:')
    run_recursive(4)
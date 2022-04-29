# Script to run the battleship game
# Final script will pull in the MDP_player.py functions
# The function from this will be run through a bootstrap to see
# if the rng beats the MDP and get the distribution

# TO DO:
## 1. Handle Errors so don't break program and can continue running
## 2. Turn into function to be read into bootstrap
## 3. Write it into bootstrap
## 4. Set player 2

# Library
import pandas as pd
import numpy as np
#import mdp_battleship.src.MDP_player

# Set board
board_size = 7

# Set player ship counts
total_ships_player_one = 6
total_ships_player_two = 6

# Set array for ship locations. Maintains ship number as well.
ship_locations_player_one = np.zeros(6,dtype=np.ndarray)
ship_locations_player_two = np.zeros(6,dtype=np.ndarray)

###### Set players
player_one = input('Is the player human or random? ').lower()
player_two = "mdp"
                   
if player_one not in ['human','random']:
    raise 'ValueError: choice must be one of human or random'
        
# Board for each player
board_player_1 = pd.DataFrame(index=range(board_size),
                              columns=range(board_size)
                             )
board_player_2 = pd.DataFrame(index=range(board_size),
                              columns=range(board_size)
                             )

# Set ship positions for player one
print(f'Ship location selection beginning. Player 1')
i=1 # Ship number
while i <= total_ships_player_one :
    # For human player, ask for input
    if player_one == 'human':
        row = int(input(f'Select row for ship {i}: '))
        col = int(input(f'Select column for ship {i}: '))
    elif player_one == 'random':
        # Select random number from 1 to 8 and take floor to give column
        row = int(np.random.uniform(1,8))
        col = int(np.random.uniform(1,8))
    
   
    if (col >= 8) or (row >= 8):
        print('Position Out of Range. Must be 1-7')
        continue
    elif isinstance(col, int) == False or isinstance(row, int) == False:
        print('Position Not Feasible. Must be integer 1-7')
        continue
    elif ('ship' in str(board_player_1.iloc[row-1,col-1])):
        print('Ship already in poistion. Please select a new one.')
        continue
    else:
        board_player_1.iloc[row-1,col-1] = f'ship {i}'
        ship_locations_player_one[i-1] = [row-1,col-1]
        i += 1
    
   
print('Player 1 Board:')
print(board_player_1)        

# Set ship positions for player 2
print(f'Ship location selection beginning. Player 2')
j = 1 # Ship number
while j <= total_ships_player_two :
    # For human player, ask for input
    # Select random number from 1 to 8 and take floor to give column
    row = int(np.random.uniform(1,8))
    col = int(np.random.uniform(1,8))
        
    if (col >= 8) or (row >= 8):
        continue
    elif ('ship' in str(board_player_2.iloc[row-1,col-1])):
        continue
    else:
        board_player_2.iloc[row-1,col-1] = f'ship {j}'
        ship_locations_player_two[j-1] = [row-1,col-1]
        j += 1
        
print('Player 2 Board:')
print(board_player_2)

# Function for player one to take turn -- Will become own script
def player_one_take_turn():
    global total_ships_player_two
    
    valid_move_taken = 0
    valid_decision = ['move ship one', 'fire']
    valid_direction = ['up','down','left','right']
    while (valid_move_taken == 0):
        # Ask player whether to move or shoot
        if player_one == 'human':
            decision = input('Choose Move: Move Ship One or Fire  ').lower()
            
            if decision not in valid_decision:
                print('Not a valid move')
                continue
                                   
                                   
            # If move, where
            if decision == 'move ship one':
                ship = input('Choose Ship Number to Move: ')
                direction = input('Choose Direction to Move One Space (Up,Down,Left,Right): ').lower()
                
                # Check ship is valid choice
                ship = int(ship)-1
                if (ship < 0) or (ship > 5):
                    print('Not a valid ship number. Must be 1 - 6')
                    continue
                elif board_player_1.iloc[ship_locations_player_one[ship][0],\
                                    ship_locations_player_one[ship][1]] == 'Destroyed':
                    print('Ship is already destroyed. Choose another ship.')
                    continue

                # Check direction is valid choice
                if direction not in valid_direction:
                    print(f'Not a valid direction. Must be one of {valid_direction}')
                    continue
                
                    
                # Remove ship from graphic
                board_player_1.iloc[ship_locations_player_one[ship][0],
                                    ship_locations_player_one[ship][1]] = np.NaN
                
                # Change location of ship
                if direction == 'up':
                    ship_locations_player_one[ship][0] = (ship_locations_player_one[ship][1]+1)%7
                elif direction == 'down':
                    ship_locations_player_one[ship][0] = (ship_locations_player_one[ship][1]-1)%7
                elif direction == 'left':
                    ship_locations_player_one[ship][1] = (ship_locations_player_one[ship][0]-1)%7
                elif direction == 'right':
                    ship_locations_player_one[ship][1] = (ship_locations_player_one[ship][1]+1)%7
                
                # Add new location to graphic
                board_player_1.iloc[ship_locations_player_one[ship][0],
                                    ship_locations_player_one[ship][1]] = f'ship {ship+1}'
                
            # If fire, where
            elif decision == 'fire':
                frow = int(input('Row to Fire On: '))
                fcol = int(input('Column to Fire On: '))
                
                if frow > 7 or frow < 1:
                    print('Invalid Row Number. Please choose 1 - 7')
                    continue
                elif fcol >7 or fcol < 1:
                    print('Invalid Column Number. Please choose 1 - 7')
                    continue
                
                # If hit, player two loses a ship   
                if ('ship' in str(board_player_2.iloc[frow-1,fcol-1])):
                    total_ships_player_two = total_ships_player_two - 1
                    board_player_2.iloc[frow-1,fcol-1] = 'Destroyed'
                    print(f'Battleship Destroyed! {total_ships_player_two} remaining.')
                else:
                    print('Missed!')
        
        # Randomized Uniform Player
        elif player_one == 'random':
            decision_num = int(np.random.uniform(0,2))
            decision = valid_decision[decision_num]
            
            # If move, where
            if decision == 'move ship one':
                ship = int(np.random.uniform(0,6))
                
                direction_num = int(np.random.uniform(0,4))
                direction = valid_direction[direction_num]
                
                # Check ship is valid choice
                if (ship < 1) or (ship > 6):
                    print('Not a valid ship number. Must be 1 - 6')
                    continue
                elif board_player_1.iloc[ship_locations_player_one[ship][0],\
                                    ship_locations_player_one[ship][1]] == 'Destroyed':
                    print('Ship is already destroyed. Choose another ship.')
                    continue
          
                # Remove ship from graphic
                board_player_1.iloc[ship_locations_player_one[ship][0],
                                    ship_locations_player_one[ship][1]] = np.NaN
                
                # Change location of ship
                if direction == 'up':
                    ship_locations_player_one[ship] = [(ship_locations_player_one[ship][1]+1)%7,
                                                        ship_locations_player_one[ship][0]]
                elif direction == 'down':
                    ship_locations_player_one[ship] = [(ship_locations_player_one[ship][1]-1)%7,
                                                       ship_locations_player_one[ship][0]]
                elif direction == 'left':
                    ship_locations_player_one[ship] = [ship_locations_player_one[ship],
                                                       (ship_locations_player_one[ship][0]-1)%7]
                elif direction == 'right':
                    ship_locations_player_one[ship] = [ship_locations_player_one[ship],
                                                       (ship_locations_player_one[ship][1]+1)%7]
                
                # Add new location to graphic
                board_player_1.iloc[ship_locations_player_one[ship][0],
                                    ship_locations_player_one[ship][1]] = f'ship {ship+1}'
                
            # If fire, where
            elif decision == 'fire':
                frow = int(np.random.uniform(0,7))
                fcol = int(np.random.uniform(0,7))
                
                if frow > 7 or frow < 1 or fcol >7 or fcol < 1:
                    continue
                
                # If hit, player two loses a ship   
                if ('ship' in str(board_player_2.iloc[frow,fcol])):
                    total_ships_player_two = total_ships_player_two - 1
                    board_player_2.iloc[frow,fcol] = 'Destroyed'
                   
                    print(f'Battleship Destroyed! {total_ships_player_two} remaining.')
                
                else:
                    print('Missed!')
            
        
        # If reach end, valid move was taken
        print(f'Player One has decided {decision}')
        valid_move_taken = 1

# Standin function for player two turn to test
def player_two_take_turn():
    global total_ships_player_one
    total_ships_player_one = total_ships_player_one - 1

# Set current player to start
current_player = 1

# Function to switch player after each turn
def switch_player():
    global current_player
    
    if current_player == 1:
        current_player = 2
    elif current_player == 2:
        current_player = 1
    else:
        raise 'Error: Player Number is not 1 or 2'

while (total_ships_player_one > 0) and (total_ships_player_two > 0):
    
    if current_player == 1:
        if player_one == 'human':
            print('Current Board:')
            print(board_player_1)
            
        player_one_take_turn()
    elif current_player == 2:
        player_two_take_turn()
    else:
        print('Issue With Current Player Variable')
        break
        
    
    print(f'Player One has {total_ships_player_one} ships remaining') 
    print(f'Player Two has {total_ships_player_two} ships remaining')
    switch_player()

if total_ships_player_one == 0:
    print('##### Game Over #####')
    print('Player 2 wins! The Markov Decision Process has bested you.')
elif total_ships_player_two == 0:
    print('##### GAME OVER #####')
    print(f'Player 1 wins! The {player_one} has beaten the Markov Decision Process.')

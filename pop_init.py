import random

#Takes a 2D-array representing the board and the newly placed queen position and outputs the new constested board 
def board_update(board, row, coloumn):
    board_length = len(board)
    #Update row
    for x in range(board_length):
        if x != coloumn:
            board[row][x] += 1
        
    #Update coloumn
    for x in range(board_length):
        if x != row:
            board[x][coloumn] += 1
        
    #up right diagonal
    next_postion = (row+1,coloumn+1)
    while (0 < next_postion[0] and next_postion[0] < board_length) and (0 < next_postion[1] and next_postion[1] < board_length):
        board[next_postion[0]][next_postion[1]] += 1
        next_postion = (next_postion[0]+1, next_postion[1]+1)
    
    #up left diagonal
    next_postion = (row+1,coloumn-1)
    while (0 < next_postion[0] and next_postion[0] < board_length) and (0 < next_postion[1] and next_postion[1] < board_length):
        board[next_postion[0]][next_postion[1]] += 1
        next_postion = (next_postion[0]+1, next_postion[1]-1)
        
    #down left diagonal
    next_postion = (row-1,coloumn-1)
    while (0 < next_postion[0] and next_postion[0] < board_length) and (0 < next_postion[1] and next_postion[1] < board_length):
        board[next_postion[0]][next_postion[1]] += 1
        next_postion = (next_postion[0]-1, next_postion[1]-1)
        
    #down right diagonal
    next_postion = (row-1,coloumn+1)
    while (0 < next_postion[0] and next_postion[0] < board_length) and (0 < next_postion[1] and next_postion[1] < board_length):
        board[next_postion[0]][next_postion[1]] += 1
        next_postion = (next_postion[0]-1, next_postion[1]+1)
        
    return board

#Takes a n-size board and generates a initial state by choosing randomly among the least contested squares. If they are not available it will go to the next best squares
def population_initliziser_heuristic(n):
    #List of available positions
    Available_coloumn_positions = [x for x in range(0,n)]
    resulting_configuration = []
    
    #State of the board. Used as the heuristisk function
    board = [[0 for _ in range(0,n)] for _ in range(0,n)]
    
    #Assume a general board and place a queen randomly in the first row
    first_queen_position = Available_coloumn_positions.pop(random.randint(0,n-1))
    resulting_configuration.append(first_queen_position)
    board = board_update(board, 0, first_queen_position)

    #randomly select one of the least contested squares for each row that is not in use. 
    for x in range(1,n):
        #Calculate the least contested squares in the row
        next_position = -1
        current_row = board[x].copy()
        while next_position == -1:
            least_contested_value = min(current_row)
            indexes_of_values = []
            #takes all indexes for the least constested squares
            indexes_of_values = [i for i, x in enumerate(board[x]) if x == least_contested_value]
            current_row = [x for x in current_row if x != least_contested_value]
            
            #randomly selects a least contested square and then checks if it is available
            while len(indexes_of_values) > 0:
                randomly_selected_position : int = indexes_of_values.pop(random.randint(0,len(indexes_of_values)-1))
                #checks if the coloumn position has not been used already
                if randomly_selected_position in Available_coloumn_positions:
                    next_position = randomly_selected_position
                    break
        
        #Update board and remove from available positions
        resulting_configuration.append(next_position)
        Available_coloumn_positions.remove(next_position)
        board = board_update(board, x, next_position)
        
    return resulting_configuration

#Takes a n-size board and generates a initial state by choosing a random coloumn each row that has not yet been placed in
def population_initliziser_random(n):
    #List of available positions
    Available_coloumn_positions = [x for x in range(0,n)]

    #randomly picks a available position to place a queen
    random.shuffle(Available_coloumn_positions)
    resulting_configuration = Available_coloumn_positions

    return resulting_configuration
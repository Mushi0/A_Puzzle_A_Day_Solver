import highspy

nb_cells = 43

def create_position(piece, lead_cell):
    '''
    Create a binary number representing the position of a piece on the board
    '''
    board = ['0'] * nb_cells
    
    x, y = lead_cell
    for (xx, yy) in piece:
        cell_x, cell_y = xx + x, yy + y
        if cell_x < 2 and cell_y > 5:
            return None
        if cell_x > 5 and cell_y > 2:
            return None
        if cell_x < 0 or cell_y < 0 or cell_x > 6 or cell_y > 6:
            return None
        
        if cell_x < 2:
            board[cell_x * 6 + cell_y] = '1'
        else:
            board[12 + (cell_x - 2) * 7 + cell_y] = '1'

    return board

def main():
    with open("Pieces.txt", "r") as file:
        pieces_data = file.readlines()
    pieces_data = [line.strip() for line in pieces_data]

    pieces_data = pieces_data + ['']
    pieces_positions = {}
    while len(pieces_data) != 0:
        # read piece shapes
        this_shape = []
        piece_nb = int(pieces_data.pop(0)[1:])
        cell = pieces_data.pop(0)
        while cell != '':
            cell = [int(x) for x in cell.split(',')]
            cell = tuple(cell)
            this_shape.append(cell)
            cell = pieces_data.pop(0)
        
        # get all the position this piece can take
        all_position_this_piece = []
        for x in range(7):
            for y in range(7):
                if x < 2 and y > 5:
                    continue
                if x > 5 and y > 2:
                    continue

                pos = create_position(this_shape, (x, y))
                if pos is not None:
                    all_position_this_piece.append(pos)
        if piece_nb not in pieces_positions:
            pieces_positions[piece_nb] = []
        pieces_positions[piece_nb] += all_position_this_piece
    
    print('Input the date you want to solve (DD-MM): ')
    date = input().strip()
    day, month = map(int, date.split('-'))

    # Optimization model definition
    where_pieces = {}
    h = highspy.Highs()
    for i, piece in pieces_positions.items():
        where_pieces[i] = h.addBinaries(len(piece))
        h.addConstr(h.qsum(where_pieces[i]) == 1)
    for j in range(nb_cells):
        if (j < 12 and j == month - 1) or (j >= 12 and j - 12 == day - 1):
            h.addConstr(h.qsum(where_pieces[i][k] * int(pieces_positions[i][k][j]) 
                            for i in pieces_positions 
                            for k in range(len(pieces_positions[i]))) <= 0)
        h.addConstr(h.qsum(where_pieces[i][k] * int(pieces_positions[i][k][j]) 
                        for i in pieces_positions 
                        for k in range(len(pieces_positions[i]))) <= 1)
    h.run()
    
    # Print the result
    solution = h.getSolution()
    info = h.getInfo()
    model_status = h.getModelStatus()
    print('Model status = ', h.modelStatusToString(model_status))
    print('Iteration count = ', info.simplex_iteration_count)
    print()
    solution_pieces = {}
    if solution:
        for i in pieces_positions:
            for k in range(len(pieces_positions[i])):
                if h.variableValue(where_pieces[i][k]) > 0.5:
                    print(f'Piece {i} at position {k}')
                    solution_pieces[i] = pieces_positions[i][k]
    else:
        print("No solution found")
    
    # make the board
    print('\n=============Solution=============')
    board = ['.'] * nb_cells
    for i, pos in solution_pieces.items():
        for j, c in enumerate(pos):
            if c == '1':
                board[j] = str(i)
    board[month - 1] = 'M'
    board[12 + day - 1] = 'D'
    for i in range(7):
        if i < 2:
            print(' '.join(board[i*6:i*6+6]))
        else:
            print(' '.join(board[12+(i-2)*7:12+(i-2)*7+7]))

if __name__ == "__main__":
    main()
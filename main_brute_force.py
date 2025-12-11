import sys

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

    return int(''.join(board), 2)

nb_solution = 0

def main():
    # print to result.txt
    sys.stdout = open("result.txt", "w")

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
    
    def search(this_piece, this_board, positions):
        global nb_solution
        
        if this_piece == 8:
            # print the board
            board = ['.'] * nb_cells
            for i, p in enumerate(positions):
                pos = bin(p)[2:]
                pos = '0' * (nb_cells - len(pos)) + pos
                for j, c in enumerate(pos):
                    if c == '1':
                        board[j] = str(i)
            month = 0
            day = 0
            for i, cell in enumerate(board):
                if cell == '.':
                    if i < 12:
                        board[i] = 'M'
                        month = i + 1
                    else:
                        board[i] = 'D'
                        day = i - 11
            if month == 0 or day == 0:
                return
            print(f'Solution {nb_solution}:')
            print(f'Date: {day}/{month}')
            for i in range(7):
                if i < 2:
                    print(' '.join(board[i*6:i*6+6]))
                else:
                    print(' '.join(board[12+(i-2)*7:12+(i-2)*7+7]))
            print()

            nb_solution += 1
            return
        
        # try all positions for the next piece
        for p in pieces_positions[this_piece]:
            if p & this_board != 0:
                continue
            search(this_piece + 1, this_board | p, positions + [p])

    search(0, 0, [])
    
    # close the file
    sys.stdout.close()

if __name__ == "__main__":
    main()
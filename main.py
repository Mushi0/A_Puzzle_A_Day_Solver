import sys
from tqdm import tqdm

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
            
    nb_solution = 0
    for p0 in tqdm(pieces_positions[0]):
        for p1 in pieces_positions[1]:
            if p1 & p0 != 0:
                continue
            for p2 in pieces_positions[2]:
                if p2 & (p0 | p1) != 0:
                    continue
                for p3 in pieces_positions[3]:
                    if p3 & (p0 | p1 | p2) != 0:
                        continue
                    for p4 in pieces_positions[4]:
                        if p4 & (p0 | p1 | p2 | p3) != 0:
                            continue
                        for p5 in pieces_positions[5]:
                            if p5 & (p0 | p1 | p2 | p3 | p4) != 0:
                                continue
                            for p6 in pieces_positions[6]:
                                if p6 & (p0 | p1 | p2 | p3 | p4 | p5) != 0:
                                    continue
                                for p7 in pieces_positions[7]:
                                    if p7 & (p0 | p1 | p2 | p3 | p4 | p5 | p6) != 0:
                                        continue
                                    # make the board
                                    board = ['.'] * nb_cells
                                    for i, p in enumerate([p0, p1, p2, p3, p4, p5, p6, p7]):
                                        pos = bin(p)[2:]
                                        pos = '0' * (nb_cells - len(pos)) + pos
                                        for j, c in enumerate(pos):
                                            if c == '1':
                                                board[j] = str(i)
                                    # check if the solution is valid and get the date
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
                                        continue
                                    
                                    print(f'Solution {nb_solution}:')
                                    print(f'Date: {day}/{month}')
                                                
                                    for i in range(7):
                                        if i < 2:
                                            print(' '.join(board[i*6:i*6+6]))
                                        else:
                                            print(' '.join(board[12+(i-2)*7:12+(i-2)*7+7]))
                                    print()

                                    nb_solution += 1
    
    # close the file
    sys.stdout.close()

if __name__ == "__main__":
    main()
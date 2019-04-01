
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
diagonal1 = [rows[k]+cols[abs(len(rows))-(k+1)] for k in range(0,len(rows))]
diagonal2 = [rows[k]+cols[k] for k in range(0,len(rows))]
diagonal_units = [diagonal1,diagonal2]
unitlist = unitlist + diagonal_units


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    for box_a in boxes:
        for box_b in peers[box_a]:
            if values[box_a] == values[box_b] and len(values[box_a]) == 2:
                commonpeers = set(peers[box_a]).intersection(set(peers[box_b]))
                for item in commonpeers:
                    for digit in values[box_a]:
                        values[item] = values[item].replace(digit,'')
    return values
    


def eliminate(values):
    for box in values:
        if len(values[box]) == 1:
            for a in peers[box]:
                if len(values[a]) == 1:
                    continue
                else:
                   values[a] = values[a].replace(values[box],'')
        else:
            continue
    return values
    


def only_choice(values):
    for unit in unitlist:
        for box in unit:
            if len(values[box]) != 1:
                for digit in values[box]:
                    possible_boxes = [boxes for boxes in unit if (digit in values[boxes] and boxes != box)]
                    if len(possible_boxes) == 0:
                        values[box] = digit
    return values 
    


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = [box for box in values.keys() if len(values[box]) == 1]
        #eliminate
        values = eliminate(values)
        #only_choice
        values = only_choice(values)
        #naked_twins
        values = naked_twins(values)
        solved_values_after = [box for box in values.keys() if len(values[box]) == 1]
        stalled = solved_values_before == solved_values_after
    return values
    

def solvedgrid(values):
    unittest = True
    for unit in unitlist:
        unitstring = ''.join(sorted(values[box] for box in unit))
        if unitstring != '123456789':
            unittest = False
    return unittest


def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all([len(values[box]) == 1 for box in boxes]):
        solved = solvedgrid(values)
        if solved:
            return values
        else:
            return False
    tobefilled = {values[box]:box for box in boxes if len(values[box]) != 1}
    min_item = min(tobefilled,key=len)
    box = tobefilled[min_item]
    for digit in values[box]:
        gridcopy = values.copy()
        gridcopy[box] = digit
        gridcopy = search(gridcopy)
        if gridcopy:
            return gridcopy
   


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    if result:
        display(result)
    else:
        print('not solved')

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

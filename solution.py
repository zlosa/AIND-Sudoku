assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'
possible_digits = '123456789'

def cross(a, b):
    return [s + t for s in a for t in b]

boxes = cross(rows, cols)
row_units = [cross(row, cols) for row in rows]
column_units = [cross(rows, col) for col in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_units = [[row + cols[rows.index(row)] for row in rows],[row + cols[sorted(rows,reverse=True).index(row)] for row in rows]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((box, [unit for unit in unitlist if box in unit]) for box in boxes)
peers = dict((box, set(sum(units[box], []))-set([box])) for box in boxes)

def assign_value(sudoku, box, value):
    sudoku[box] = value
    if len(value) == 1:
        assignments.append(sudoku.copy())
    return sudoku

def solved_boxes(sudoku):
    return len([box for box in sudoku.keys() if len(sudoku[box]) == 1])

def update_dict(dictionary, key, value):
    dictionary.update({key: value})
    return dictionary

def grid_values(grid):
    assert len(grid) == 81, "The lenght of `grid` should be 81. A 9x9 sudoku"
    chars = []
    for char in grid:
        if char in possible_digits: chars.append(char)
        if char == '.': chars.append(possible_digits)
    return dict(zip(boxes, chars))

def display(values):
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in rows:
        print(''.join(values[row + col].center(width) + ('|' if col in '36' else '') for col in cols))
        if row in 'CF': print(line)
    return

def return_pairs(sudoku):
    return [box for box in boxes if len(sudoku[box]) == 2]

def naked_twins(sudoku):
    pairs = return_pairs(sudoku)
    for box in pairs:
        for unit in units[box]:
            peers_pairs = set(unit).intersection(set(peers[box])).intersection(set(pairs))
            for peer in peers_pairs:
                if sudoku[box] == sudoku[peer]:
                    for item in set(unit).difference(set([box, peer])):
                        t_1 = sudoku[box][0]
                        t_2 = sudoku[box][1]
                        if t_1 in sudoku[item]:
                            sudoku = assign_value(sudoku, item, sudoku[item].replace(t_1, ''))
                        if t_2 in sudoku[item]:
                            assign_value(sudoku, item, sudoku[item].replace(t_2, ''))

    return sudoku


def eliminate(sudoku):
    solved_values = [box for box in sudoku.keys() if len(sudoku[box]) == 1]
    for box in solved_values:
        value = sudoku[box]
        for peer in peers[box]:
            assign_value(sudoku, peer, sudoku[peer].replace(value, ''))

    return sudoku

def only_choice(sudoku):
    for unit in unitlist:
        for value in possible_digits:
            value_places = [box for box in unit if value in sudoku[box]]
            if len(value_places) == 1:
                assign_value(sudoku, value_places[0], value)

    return sudoku


def reduce_puzzle(sudoku):
    working = True
    while working:
        solved_values_prior = solved_boxes(sudoku)
        sudoku = eliminate(sudoku)
        sudoku = only_choice(sudoku)
        sudoku = naked_twins(sudoku)
        solved_values_after = solved_boxes(sudoku)
        working = solved_values_prior != solved_values_after

        if len([box for box in sudoku.keys() if len(sudoku[box]) == 0]):
            return False
    return sudoku

def solve(grid):
    return search(grid_values(grid))

def search(sudoku):
    values = reduce_puzzle(sudoku)
    if values == False:
        return False
    
    if all(len(values[s]) == 1 for s in boxes):
        return values

    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new = values.copy()
        new[s] = value
        work = search(new)
        if work:
            return work

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'
possible_digits = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

"""def naked_twins(values):
    Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
def naked_twins(sudoku):
    """Eliminates values using the naked twins strategy.
    Args:
        sudoku: A dict representation of the sudoku
    Returns:
        A dict representation of the sudoku with the
        naked twins deleted from it's peers.
    """
    pair_list = get_pairs(sudoku)
    for box in pair_list:
        for unit in units[box]:
            # Find the peers in the unit that contains 2 digits
            # but is not the box itself
            peers_with_pairs = set(unit).intersection(set(peers[box])).intersection(set(pair_list))

            for peer in peers_with_pairs:
                if sudoku[box] == sudoku[peer]:
                    for item in set(unit).difference(set([box, peer])):
                        digit_1 = sudoku[box][0]
                        digit_2 = sudoku[box][1]

                        if digit_1 in sudoku[item]:
                            sudoku = assign_value(sudoku, item, sudoku[item].replace(digit_1, ''))
                        if digit_2 in sudoku[item]:
                            assign_value(sudoku, item, sudoku[item].replace(digit_2, ''))

    return sudoku

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def cross(a, b):
    """
    "Cross product of elements in A and elements in B."
    
    Return a list with all concatenations of a letter in
    `a` with a letter in `b`
    Args:
        a: A string
        b: A string
    Returns:
        A list formed by all the possible concatenations of a
        letter in `a` with a letter in `b`
    """
    return [s + t for s in a for t in b]

def grid_values(grid):
    """
    Returns a dict that represents a sudoku.
    Args:
        grid: A string with the starting numbers
        for all the boxes in a sudoku. Empty boxes
        can be represented as dots `.`.
        Example: `'..3.2.6.'...`
    Returns:
        A dict that represents a sudoku. The keys
        will be the boxes labels and it's value will be the number
        or a dot `.` if the box is empty.
    """
    assert len(grid) == 81, "The lenght of `grid` should be 81. A 9x9 sudoku"
    chars = []
    for char in grid:
        if char in possible_digits: chars.append(char)
        if char == '.': chars.append(possible_digits)
    return dict(zip(boxes, chars))

def display(values):
    """
    Prints the values of a sudoku as a 2-D grid.
    Args:
        values: A dict representing a sodoku.
    Returns:
        `None`
        
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in rows:
        print(''.join(values[row + col].center(width) + ('|' if col in '36' else '') for col in cols))
        if row in 'CF': print(line)
    return

boxes = cross(rows, cols)
row_units = [cross(row, cols) for row in rows]
column_units = [cross(rows, col) for col in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_units = [[row + cols[rows.index(row)] for row in rows],[row + cols[sorted(rows,reverse=True).index(row)] for row in rows]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((box, [unit for unit in unitlist if box in unit]) for box in boxes)
peers = dict((box, set(sum(units[box], []))-set([box])) for box in boxes)


def eliminate(sudoku):
    """
    Returns a sudoku dict after applying the eliminate technique.
    Args:
        sudoku: A dict representing the sudoku. It'll contain
        in each box the value of it, or the possible values.
    Returns:
        A sudoku dict after applying the eliminate technique in all
        the boxes.
    """
    solved_values = [box for box in sudoku.keys() if len(sudoku[box]) == 1]
    for box in solved_values:
        value = sudoku[box]
        for peer in peers[box]:
            assign_value(sudoku, peer, sudoku[peer].replace(value, ''))


    return sudoku

def only_choice(sudoku):
    """
    It runs through all the units of a sudoku
    and it applies the only choice technique.
    Args:
        sudoku: A dict representing the sudoku.
    Returns:
        A sudoku dict after applying the only choice technique.
    """
    for unit in unitlist:
        for value in possible_digits:
            value_places = [box for box in unit if value in sudoku[box]]
            if len(value_places) == 1:
                assign_value(sudoku, value_places[0], value)

    return sudoku


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(sudoku):
    """
    Uses depth search first and propagaation to find a solution for the sudoku
    Args:
        sudoku: A dict representation of a sudoku
    Returns:
        A dict representation of the sudoku solved
    """
    sudoku = reduce_puzzle(sudoku)
    if sudoku is False:
        return False

    # Check if the sudoku is solved
    if all([len(sudoku[box]) == 1 for box in boxes]):
        return sudoku

    n, min_box = min((len(sudoku[box]), box) for box in boxes if len(sudoku[box]) > 1)

    return some(search(update_dict(sudoku.copy(), min_box, digit)) for digit in sudoku[min_box])

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

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

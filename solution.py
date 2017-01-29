assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'
possible_digits = '123456789'

def cross(a, b):
    return [s + t for s in a for t in b]

def assign_value(sudoku, box, value):
    """Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    Args:
        sudoku: A dict representation of the sudoku.
        box: The box to be updated.
        value: The value to update
    Returns:
        Returns the sudoku dict updated.
    """
    sudoku[box] = value
    if len(value) == 1:
        assignments.append(sudoku.copy())
    return sudoku

def get_pairs(sudoku):
    """Return all the boxes with just 2 digits"""
    return [box for box in boxes if len(sudoku[box]) == 2]

def solved_boxes(sudoku):
    """Returns the number of boxes solved in a sudoku"""
    return len([box for box in sudoku.keys() if len(sudoku[box]) == 1])

def update_dict(dictionary, key, value):
    """Updates the dict `dictionary` and returns the dict"""
    dictionary.update({key: value})
    return dictionary

def some(seq):
    """Return some element of `seq` that is `True` http://norvig.com/sudoku.html"""
    for e in seq:
        if e: return e
    return False

# Display functions
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


def reduce_puzzle(sudoku):
    """
    Uses constrain propagation to reduce the search space
    Args:
        sudoku: A dict representing the sudoku.
    Returns:
        A sudoku dict solved or partially solved
    """
    improving = True
    while improving:
        solved_values = solved_boxes(sudoku)

        sudoku = eliminate(sudoku)
        sudoku = only_choice(sudoku)
        sudoku = naked_twins(sudoku)

        solved_values_after = solved_boxes(sudoku)

        improving = solved_values != solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in sudoku.keys() if len(sudoku[box]) == 0]):
            return False
    return sudoku

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

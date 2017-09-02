import collections

assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'
digits = '123456789'


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [r + c for r in A for c in B]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diag_units = [r + c for r, c in zip(rows, cols)]
diag_units_neg = [r + c for r, c in zip(rows, cols[::-1])]
unitlist = row_units + column_units + square_units + [diag_units, diag_units_neg]
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        nt = [item for item, count in collections.Counter((values[u] for u in unit)).items() if
              count == 2 and len(item) == 2]
        # if found naked twins, remove them from rest of the unit
        if nt:
            nt_found = nt[0]
            for u in unit:
                if values[u] != nt_found:
                    values[u]= values[u].replace(nt_found[0], '')
                    values[u]= values[u].replace(nt_found[1], '')
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value
            will be '123456789'.
    """
    values = {}
    for b, v in zip(boxes, grid):
        if v == '.':
            values[b] = '123456789'
        else:
            values[b] = v
    return values


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one
    box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                # values[dplaces[0]] = digit
                values = assign_value(values, dplaces[0], digit)
    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available
    values, return False.
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


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    # Choose one of the unfilled squares with the fewest possibilities
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!
    n, s = min((len(s), s) for s in values.keys() if len(values[s]) > 1)
    possible_v = values[s]
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (
    # not False), return that answer!
    for v in possible_v:
        pvalues = dict(values)
        pvalues[s] = v
        res = search(pvalues)
        if res:
            return res


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52
            .............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    res = search(values)
    return res


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52' \
                       '.............3'
    display(solve(diag_sudoku_grid))

    # print(assignments)
    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print(
            'We could not visualize your board due to a pygame issue. Not a problem! It isnot a requirement.')

assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

boxes = cross(rows, cols) # 81
row_units = [cross(r, cols) for r in rows]  # 9*9
column_units = [cross(rows, c) for c in cols]  # 9*9
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#unitlist = row_units + column_units + square_units  # 27*9
#units = {s: [u for u in unitlist if s in u] for s in boxes} # 81 keys*9
#peers = {s: set(sum(units[s],[]))-set([s]) for s in boxes}  # 81 keys*20

diag_units = [["A1","B2","C3","D4","E5","F6","G7","H8","I9"],
          ["A9","B8","C7","D6","E5","F4","G3","H2","I1"]]
unitlist = row_units + column_units + square_units + diag_units # 29*9
units = {s: [u for u in unitlist if s in u] for s in boxes} # 81 keys*10
peers = {s: set(sum(units[s],[]))-set([s]) for s in boxes}  # 81 keys*20


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
    """
    Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    # print("naked")
    for unit in unitlist:
        size2 = [box for box in unit if len(values[box])==2]
        dic = {}
        for box in size2:
            target = values[box]
            if len(target) == 1:
                continue
            if target not in dic:
                dic[target] = box
            else:
                for each in unit:
                    digit = values[each]
                    if len(digit) > 1 and digit != target:
                        values[each]= digit.replace(target[0],"")
                        values[each]= values[each].replace(target[1],"")
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    #print("grid_values")
    values = []
    for  each in grid:
        if each == ".":
            values.append("123456789")
        elif each in "123456789":
            values.append(each)
    # boxes = cross(rows,cols)
    return dict(zip(boxes,values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    '''
    From the peers, remove the digits that has been solved_values
    '''
    #print("eliminate")
    solved_values = [box for box in values.keys() if len(values[box])==1]
    #print(len(solved_values))
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer]= values[peer].replace(digit,"")
    return values

def only_choice(values):
    #print("only_choice")
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        #print("reduce_puzzle")
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    '''Using depth-first search and propagation, try all possible values.'''

    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    '''
    solve the diagonal sokudo.
    input: string with length of 81
    output: dictionary
    '''
    #print("solve")
    values = grid_values(grid)
    #display(values)
    values = search(values)
    return values

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

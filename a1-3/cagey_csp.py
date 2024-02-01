# =============================
# Student Names: Daniel Lister, Jackson Walker, Benjamin Falkner
# Group ID: 40
# Date: January 22 2024
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.

'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all variables in the given csp. If you are returning an entire grid's worth of variables
they should be arranged in a linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 20/100 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *
import itertools

def binary_ne_grid(cagey_grid):
    n, _ = cagey_grid  # Grid size from the puzzle input.

    csp = CSP("Cagey Binary")  # Initialize CSP for Cagey grid.

    # Create grid variables with domains set from 1 to n.
    vars = [[Variable(f'V{i}{j}', domain=list(range(1, n+1))) for j in range(n)] for i in range(n)]
    for i in range(n):  # Add each variable to the CSP.
        for j in range(n):
            csp.add_var(vars[i][j])

    # Add binary not-equal constraints for rows and columns.
    for i in range(n):
        for j in range(n):
            for k in range(j + 1, n):  # Iterate over pairs of variables.
                # Row constraint to ensure different values across the row.
                row_con = Constraint(f"Row-{i}-{j}-{k}", [vars[i][j], vars[i][k]])
                # Add satisfying tuples for the row constraint (all unique pairs).
                row_con.add_satisfying_tuples([(x, y) for x in range(1, n + 1) for y in range(1, n + 1) if x != y])
                csp.add_constraint(row_con)  # Enforce row uniqueness in the CSP.

                # Column constraint to ensure different values down the column.
                col_con = Constraint(f"Col-{i}-{j}-{k}", [vars[j][i], vars[k][i]])
                # Add satisfying tuples for the column constraint (all unique pairs).
                col_con.add_satisfying_tuples([(x, y) for x in range(1, n + 1) for y in range(1, n + 1) if x != y])
                csp.add_constraint(col_con)  # Enforce column uniqueness in the CSP.
    
    return csp, vars  # Return configured CSP and variable grid for Cagey puzzle.



def all_diff_tuples(size):
    # Generate all tuples of size 'size' with all distinct elements
    return [tup for tup in itertools.permutations(range(1, size+1), size)]

def nary_ad_grid(cagey_grid):
    n, _ = cagey_grid  # Extract grid size from input, ignoring cage constraints.

    csp = CSP("Cagey Binary")  # Create CSP instance for the Cagey puzzle.

    # Initialize grid variables with domains from 1 to n.
    vars = [[Variable(f'V{i}{j}', domain=list(range(1, n+1))) for j in range(n)] for i in range(n)]
    for i in range(n):  # Add variables to the CSP.
        for j in range(n):
            csp.add_var(vars[i][j])

    for i in range(n):
        row_vars = vars[i]  # Collect variables for the ith row.
        row_con = Constraint(f"Row-{i}-alldiff", row_vars)  # Create all-different constraint for the row.
        row_con.add_satisfying_tuples(all_diff_tuples(n))  # Generate and add satisfying tuples for the constraint.
        csp.add_constraint(row_con)  # Add row constraint to the CSP.

        col_vars = [vars[x][i] for x in range(n)]  # Should collect variables for the ith column (correction for clarity).
        col_con = Constraint(f"Col-{i}-alldiff", col_vars)
        col_con.add_satisfying_tuples(all_diff_tuples(n))  # Generate and add satisfying tuples for the constraint.
        csp.add_constraint(col_con)  # Add column constraint to the CSP.

    return csp, vars  # Return CSP model and variables for Cagey puzzle.

def cagey_csp_model(cagey_grid):
    n, cages = cagey_grid  # Extract grid size and cage definitions.

    csp = CSP("cagey grid")  # Initialize CSP for the Cagey puzzle.

    # Initialize grid variables with domains from 1 to n, adjusting indices for 1-based.
    vars = [[Variable(f'Cell{i}{j}', domain=list(range(1, n+1))) for j in range(1, n+1)] for i in range(1, n+1)]
    for i in range(1, n+1):
        for j in range(1, n+1):
            csp.add_var(vars[i-1][j-1])  # Add variables to CSP, correcting index to 0-based for list.

    # Loop through each cage to set up constraints.
    for cage in cages:
        target, cells, op = cage  # Extract target value, cells, and operation of the cage.

        # Create a variable for cage operations, initially allowing all operations plus a 'f' for flexibility.
        op_var_name = f'Cage_op({target}:{op}:[{", ".join(f"Var-Cell({cell[0]},{cell[1]})" for cell in cells)}])'
        op_var = Variable(op_var_name, ['+', '-', '/', '*', 'f'])
        csp.add_var(op_var)  # Add operation variable to CSP.

        # Gather variables corresponding to each cell in the cage, starting with the operation variable.
        con_vars = [op_var] + [vars[cell[0] - 1][cell[1] - 1] for cell in cells]  # Correcting collection of cell variables.

        # Create a constraint for the cage using these variables.
        con = Constraint(f"Cage{cells}", con_vars)

        # Generate satisfying tuples for the constraint based on the operation and target value.
        sat_tup = find_sat_tuples(n, target, con_vars, op)



def find_sat_tuples(n, target, cage_vars, op):
    sat_tup = []
    cage_size = len(cage_vars) -1

    # Generate all possible combinations of values
    all_combinations = itertools.product(range(1, n + 1), repeat=cage_size)

    for combo in all_combinations:
        if op == '+':
            if sum(combo) == target:
                sat_tup.append((op, ) +combo)
        elif op == '-':
            # Subtraction: Check all pairs in the combo for the target difference
            for i in range(cage_size):
                for j in range(cage_size):
                    if i != j and abs(combo[i] - combo[j]) == target:
                        sat_tup.append((op, ) + combo)
        elif op == '*':
            product = 1
            for num in combo:
                product *= num
            if product == target:
                sat_tup.append((op, ) +combo)
        elif op == '/':
            # Division: Check all pairs in the combo for the target quotient
            for i in range(cage_size):
                for j in range(cage_size):
                    if i != j and (combo[i] / combo[j] == target or combo[j] / combo[i] == target):
                        sat_tup.append((op, ) +combo)
        elif op == '?':
            # If operation is unknown, consider all combinations
            sat_tup.append((op, ) +combo)

    # Remove duplicates if any
 

    sat_tup = list(set(sat_tup))

    return sat_tup

        

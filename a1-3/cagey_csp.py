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
    
    n, _ = cagey_grid

    csp = CSP("Cagey Binary")

    vars = [[Variable(f'V{i}{j}', domain=list(range(1, n+1))) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            csp.add_var(vars[i][j])


    for i in range(n):
        for j in range(n):
            for k in range(j + 1, n):
                row_con = Constraint(f"Row-{i}-{j}-{k}", [vars[i][j], vars[i][k]])
                row_con.add_satisfying_tuples([(x, y) for x in range(1, n + 1) for y in range(1, n + 1) if x != y])
                csp.add_constraint(row_con)

                col_con = Constraint(f"Col-{i}-{j}-{k}", [vars[j][i], vars[k][i]])
                col_con.add_satisfying_tuples([(x, y) for x in range(1, n + 1) for y in range(1, n + 1) if x != y])
                csp.add_constraint(col_con)
    
    return csp,vars


def all_diff_tuples(size):
    # Generate all tuples of size 'size' with all distinct elements
    return [tup for tup in itertools.permutations(range(1, size+1), size)]

def nary_ad_grid(cagey_grid):

    n, _ = cagey_grid

    csp = CSP("Cagey Binary")

    vars = [[Variable(f'V{i}{j}', domain=list(range(1, n+1))) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            csp.add_var(vars[i][j])

    

    for i in range(n):
        row_vars = vars[i]
        row_con = Constraint(f"Row-{i}-alldiff", row_vars)
        row_con.add_satisfying_tuples(all_diff_tuples(n))

        csp.add_constraint(row_con)

        col_vars = vars[j]
        col_con = Constraint(f"Row-{j}-alldiff", col_vars)
        col_con.add_satisfying_tuples(all_diff_tuples(n))

        csp.add_constraint(col_con)


        
    return csp,vars

    
            

def cagey_csp_model(cagey_grid):
    n, cages = cagey_grid

    # Create the CSP object.
    csp = CSP("cagey grid")

    # Initialize the variables with the expected naming convention.
    vars = [[Variable(f'Cell{i}{j}', domain=list(range(1, n+1))) for j in range(1, n+1)] for i in range(1, n+1)]
    for i in range(1, n+1):
        for j in range(1, n+1):
            # Add each variable to the CSP.
            csp.add_var(vars[i-1][j-1])

   
    # Create and add constraints for each cage.
    for cage in cages:
        target, cells, op = cage
        
       # Create a special Variable object for the operation
        op_var_name = f'Cage_op({target}:{op}:[{", ".join(f"Var-Cell({cell[0]},{cell[1]})" for cell in cells)}])'
        

        op_var = Variable(op_var_name, ['+', '-', '/', '*', 'f'])
        csp.add_var(op_var)
        # Fetch the corresponding variable objects for each cell in the cage and prepend the operation variable.
        con_vars = [op_var]  # Start with a list containing the first element
        con_vars.extend(vars[cell[0] - 1][cell[1] - 1] for cell in cells)  # Extend the list with the list comprehension


        # Create a constraint with these variables.
        con = Constraint(f"Cage{cells}", con_vars)

        # Find satisfying tuples for the constraint.
        sat_tup = find_sat_tuples(n, target, con_vars, op)
        
        # Add satisfying tuples to the constraint and add it to the CSP.
        con.add_satisfying_tuples(sat_tup)
        csp.add_constraint(con)

    
        

    
       
    return csp, csp.get_all_vars()


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

        
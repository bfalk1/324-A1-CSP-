# =============================
# Student Names: Daniel Lister, Jackson Walker, Benjamin Falkner
# Group ID: 40
# Date: January 22 2024
# =============================
# CISC 352 - W23
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return variables according to the Degree Heuristic '''
    result = csp.get_all_unasgn_vars()[0]  # Start with the first unassigned variable as a default.
    temp = 0  # Temporary variable to hold the max count of constraints involving unassigned variables.

    for var in csp.get_all_unasgn_vars():  # Iterate over all unassigned variables.
        counter = 0  # Count constraints involving 'var' that also involve other unassigned variables.
        for c in csp.get_cons_with_var(var):  # Get constraints that include 'var'.
            if c.get_n_unasgn() > 1:  # Count only constraints with more than one unassigned variable.
                counter += 1
        if counter > temp:  # If 'var' is involved in more such constraints than previous max,
            result = var  # update 'result' to be 'var'.
            temp = counter  # Update 'temp' to reflect the new maximum.

    return result  # Return the variable involved in the maximum number of applicable constraints.
   
def ord_mrv(csp):
    # Initialize 'temp' with the first variable, assuming all variables initially have the same chance.
    temp = csp.get_all_vars()[0]
    
    for var in csp.get_all_unasgn_vars():  # Iterate through all unassigned variables in the CSP.
        cur_domain_size = var.cur_domain_size()  # Get the current number of legal values for 'var'.
        
        # Check if 'var' has fewer legal values than 'temp', indicating it's more constrained.
        if cur_domain_size < temp.cur_domain_size():
            temp = var  # Update 'temp' to the new most constrained variable.
            
    return temp  # Return the variable with the fewest legal values remaining.


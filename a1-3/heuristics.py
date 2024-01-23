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
    result = csp.get_all_unasgn_vars()[0]
    temp = 0

    for var in csp.get_all_unasgn_vars():
        counter = 0
        for c in csp.get_cons_with_var(var):
            if c.get_n_unasgn() > 1:
                counter += 1
        if counter > temp:
            result = var
            temp = counter

    return result




def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    temp = csp.get_all_vars()[0]
    for var in csp.get_all_unasgn_vars():
        cur_domain_size = var.cur_domain_size()
        if cur_domain_size < temp.cur_domain_size():
            temp = var
    return temp

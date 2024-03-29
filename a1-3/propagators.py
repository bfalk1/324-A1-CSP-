# =============================
# Student Names: Daniel Lister, Jackson Walker, Benjamin Falkner
# Group ID: 40
# Date: January 22 2024
# =============================
# CISC 352 - W23
# propagators.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          propagator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

import itertools

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check_tuple(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
   '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
   
    pruned = []  # Initialize list for tracking pruned values.
    if not newVar:  # No action needed if no variable is recently assigned.
        return True, pruned
    for c in csp.get_cons_with_var(newVar):  # Iterate over constraints affected by newVar.
        if c.get_n_unasgn() == 1:  # Target constraints with one variable left to assign.
            var = c.get_unasgn_vars()[0]  # Identify the variable to potentially prune.
            cur_domain = var.cur_domain()  # Access the domain before potential pruning.
            cur_domain_copy = cur_domain.copy()  # Worfk on a copy to avoid iteration issues.

            for val in cur_domain_copy:  # Evaluate each domain value for consistency.
                if not c.check_var_val(var, val):  # Prune if value violates the constraint.
                    var.prune_value(val)  # Execute pruning to enforce consistency.
                    pruned.append((var, val))  # Log pruning for backtrack restoration.
                    cur_domain.remove(val)  # Update domain reflectively after pruning.

            if len(cur_domain) == 0:  # Check for an empty domain indicating a dead-end.
                return False, pruned

    return True, pruned  # Return success if forward checking imposes no dead-ends.

def prop_GAC(csp, newVar=None):
     '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
   
    pruned = []  # List to keep track of pruned variable-value pairs.
    if not newVar:
        # Initial GAC enforcement: process all constraints to establish GAC.
        for con in csp.get_all_cons():
            pruned += remove_inconsistent(con)  # Prune inconsistent values from all constraints.
    else:
        # GAC enforcement for constraints involving the recently assigned variable.
        for con in csp.get_cons_with_var(newVar):
            pruned += remove_inconsistent(con)  # Prune values only from constraints affected by newVar.

    return True, pruned  # Return success and any pruned variable-value pairs.

def remove_inconsistent(con):
    pruned = []
    for var in con.get_unasgn_vars():
        cur_domain = var.cur_domain()
        cur_domain_copy = cur_domain.copy()

        for val in cur_domain_copy:
            # If the value violates a constraint, prune it
            if not con.check_var_val(var, val):
                var.prune_value(val)
                pruned.append((var, val))
                cur_domain.remove(val)

    return pruned



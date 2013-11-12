# -*- coding: utf-8 -*-
'''
Created on 15.02.2013

@author: natalia
'''
import copy
from common import util, replace, equiv
from solutions import solbuild

def is_correct(student_formula, system_expressions, notations, solution_point):
       
    for system_expression in system_expressions:
        pattern                  = student_formula.split('=')[1]
        expression               = system_expression.get_expression().split('=')[1]

        pattern_notations_set    = set(replace.met_notations(pattern, notations))
        expression_notations_set = set(replace.met_notations(expression, notations))
        notations_to_replace     = list(expression_notations_set.difference(pattern_notations_set))
        
        pattern                  = replace.replace_notations_to_values(pattern, notations_to_replace, solution_point)
        expression               = replace.replace_notations_to_values(expression, notations_to_replace, solution_point)
        
        if (equiv.check_expression (pattern, expression) == 1):
            return True

    return False

def construct_system_expressions(calc_relations, notations, solutions_groups, sought_variable, variables, vectors, initiators_set=set()):
    system_expressions = []
    coordinates = solbuild.get_coordinates(calc_relations, vectors, initiators_set)
    
    for group_of_solutions in solutions_groups:
        for solution in group_of_solutions:
            goal_variables = solution.get_goal_variables()
            calc_ids       = solution.get_calc_ids()
            
            if sought_variable in goal_variables:
                start_pos            = goal_variables.index(sought_variable)
                calc_relation        = util.get_calc_relation_by_id(calc_relations, calc_ids[start_pos])
                expression           = calc_relation.formula_text
                notations_to_replace = copy.deepcopy(calc_relation.left_part)
             
                if expression_is_found(expression, notations, variables):
                    used_calc_ids = [calc_ids[start_pos]]
                    system_expressions.append(SystemExpression(expression, used_calc_ids))
                    
                else:
                    expression = get_system_expression(calc_relations, notations, variables, solutions_groups, notations_to_replace, expression, start_pos, calc_ids, coordinates, vectors)
                    system_expressions.append(expression)
         
    return system_expressions
    
class SystemExpression(object):
    
    def __init__(self, expression, calc_ids):
        self.expression = expression
        self.calc_ids = calc_ids
        
    def get_expression(self):
        return self.expression
    
    def get_calc_ids(self):
        return self.calc_ids
    
def get_system_expression(calc_relations, notations, variables, solutions_groups, notations_to_replace, expression, start_pos, calc_ids, coordinates, vectors):
    used_calc_ids = []
    for i in range(start_pos + 1, len(calc_ids)): 
        calc_relation   = util.get_calc_relation_by_id(calc_relations, calc_ids[i])
        used_calc_ids.append(calc_ids[i])
        notation        = calc_relation.right_part
        expression_part = calc_relation.formula_text.split('=')[1]
        expression      = expression.replace(notation, '(' + expression_part + ')')
        pos             = notations_to_replace.index(notation)
        del notations_to_replace[pos]
        notations_to_replace.extend(calc_relation.left_part)
        if expression_is_found(expression, notations, variables):
            used_calc_ids = [calc_ids[start_pos]] + used_calc_ids
            return SystemExpression(expression, used_calc_ids)
      
    if set(notations_to_replace).issubset(coordinates):
        vector_name = get_vector_name(calc_relations, notations_to_replace)
        expr1 = get_vector_expr_from_coordinates(notations_to_replace)
        expressions = []
        
        if len(vector_name) > 0:
            vector_expressions = construct_system_expressions(calc_relations, notations, solutions_groups, vector_name, variables, vectors, notations_to_replace)   
            expr1 = get_vector_expr_from_coordinates(notations_to_replace)
            expr2 = vector_expressions[0].get_expression().split('=')[1]
            matches = equiv.match_vector_coordinates(notations, expr1, expr2)
            if (len(matches) > 0):
                for k,v in matches.iteritems():
                    expression = expression.replace(k, '(' + v + ')')
                if expression_is_found(expression, notations, variables):
                    used_calc_ids = [calc_ids[start_pos]] + used_calc_ids + vector_expressions[0].get_calc_ids()
                    return SystemExpression(expression, used_calc_ids)
                
    return SystemExpression('', [])

def get_vector_name(calc_relations, notations):
    for calc_rel in calc_relations:
        #тут нужно усложнять
        if (calc_rel.type == 'vector_def' and set(calc_rel.left_part).issubset(notations)):
            return calc_rel.right_part
    return ''

def get_vector_expr_from_coordinates(notations):
    expr = '(['
    for notation in notations:
        expr = expr + notation + ';'
    expr = expr[:-1] + '])'
    return expr
        
def expression_is_found(expression, notations, variables):
    
    found = False
    if '=' in expression:
        expression_set = set(replace.met_notations(expression.split('=')[1], notations))
        variables_set      = set(variables)
        if (expression_set.issuperset(variables_set)):
            found = True
    return found

def get_solutions(soltree, calc_relations):
    
    #пока дерево строится так, что goal variable соответствует наименьший ключ словаря. а вообще наверное это может быть не так.
    steps = get_new_steps(soltree, min(soltree.keys()))
    prev_len = 0
    curr_len = cumulative_length(steps)
    while (curr_len > prev_len):
        new_iteration_steps = []
        for step in steps:
            new_steps = get_new_steps(soltree, step[len(step)-1])
            if (len(new_steps) > 0):
                for new_step in new_steps:
                    #здесь осторожно...
                    new_iteration_steps.append(step[:-1] + new_step)
            else:
                new_iteration_steps.append(step)
                
        prev_len = cumulative_length(steps)
        steps    = new_iteration_steps
        curr_len = cumulative_length(steps)
      
    #получается такая штука - [[0, 3], [0, 4, 9, 10], [0, 11, 5, 7, 8], [0, 11, 6, 9, 10]] - надо из списков убирать первый элемент
    calc_ids_lists = map(lambda x: x[1:],steps)
    solutions = []
    for ids_list in calc_ids_lists:
        goal_variables = []
        for calc_id in ids_list:
            goal_variables.append(util.get_calc_relation_by_id(calc_relations, calc_id).right_part)
            
        solutions.append(Solution(ids_list, goal_variables))
            
    return solutions

class Solution(object):
    
    def __init__(self, calc_ids, goal_variables):
        self.calc_ids = calc_ids
        self.goal_variables = goal_variables
        
    def get_calc_ids(self):
        return self.calc_ids
    
    def get_goal_variables(self):
        return self.goal_variables
    
    def set_goal_variables(self, goal_variables):
        self.goal_variables = goal_variables
    
    def length(self):
        return len(self.calc_ids)

def get_new_steps(solutions_graph, calc_id):
    result = []
    if calc_id in solutions_graph:
        calc_ids_lists = solutions_graph[calc_id]
        for calc_id_list in calc_ids_lists:
            new_step = [calc_id] + calc_id_list
            result.append(new_step)
    return result

def cumulative_length(lst):
    return sum(map(lambda x: len(x), lst))
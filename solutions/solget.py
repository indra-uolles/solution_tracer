# -*- coding: utf-8 -*-
'''
Created on 15.02.2013

@author: natalia
'''
import copy
from common import util, replace, equiv

def is_correct(student_formula, system_expressions, notations, solution_point):
       
    for system_expression in system_expressions:
        pattern                  = student_formula.split('=')[1]
        expression               = system_expression.split('=')[1]

        pattern_notations_set    = set(replace.met_notations(pattern, notations))
        expression_notations_set = set(replace.met_notations(expression, notations))
        notations_to_replace     = list(expression_notations_set.difference(pattern_notations_set))
        
        pattern                  = replace.replace_notations_to_values(pattern, notations_to_replace, solution_point)
        expression               = replace.replace_notations_to_values(expression, notations_to_replace, solution_point)
        
        if (equiv.check_expression (pattern, expression) == 1):
            return True

    return False

def construct_expressions(calc_relations, notations, solutions, sought_variable, variables):
    expressions = []
    
    for solution in solutions:
        goal_variables = solution.get_goal_variables()
        calc_ids       = solution.get_calc_ids()
        
        if sought_variable in goal_variables:
            start_pos            = goal_variables.index(sought_variable)
            calc_relation        = util.get_calc_relation_by_id(calc_relations, calc_ids[start_pos])
            expression           = calc_relation.formula_text
            notations_to_replace = copy.deepcopy(calc_relation.left_part)
         
            if expression_is_found(expression, notations, variables):
                expressions.append(expression)
                
            else:
                try:
                    #отвалится на "по с можно вычислить (с,c)". тут нужно вводить более сложную структуру - типа само пропускаем, как-то связываем дальше
                    expression = construct_expression(calc_relations, notations, variables, notations_to_replace, expression, start_pos, calc_ids)
                    expressions.append(expression)
                except:
                    pass
         
        return expressions
    
def construct_expression(calc_relations, notations, variables, notations_to_replace, expression, start_pos, calc_ids):
    for i in range(start_pos + 1, len(calc_ids)): 
        calc_relation   = util.get_calc_relation_by_id(calc_relations, calc_ids[i])
        notation        = calc_relation.right_part
        expression_part = calc_relation.formula_text.split('=')[1]
        expression      = expression.replace(notation, '(' + expression_part + ')')
        pos             = notations_to_replace.index(notation)
        del notations_to_replace[pos]
        notations_to_replace.extend(calc_relation.left_part)
        if expression_is_found(expression, notations, variables):
            return expression
    return ''
        
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
# -*- coding: utf-8 -*-
'''
Created on 15.02.2013

@author: natalia
'''
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
        
        if (equiv.check_expression (pattern, expression) == 0):
            return True

    return False

def form_expressions(solutions, calc_relations, notations, known_variables):
    
    result = []
    for solution in solutions:
        
        expression = form_expression(solution, calc_relations, notations, known_variables)
        if (len(expression) > 0):
            result.append(expression)

    return result

def form_expression(solution, calc_relations, notations, known_variables):
    
        calc_relation        = util.get_calc_relation_by_id(calc_relations, solution[0])
        expression           = calc_relation.formula_text
        notations_to_replace = calc_relation.left_part
        
        if expression_is_found(expression, notations, known_variables):
            return expression
        
        try:
            #отвалится на "по с можно вычислить (с,c)". тут нужно вводить более сложную структуру - типа само пропускаем, как-то связываем дальше
            for i in range(1, len(solution)): 
                calc_relation = util.get_calc_relation_by_id(calc_relations, solution[i])
                notation = calc_relation.right_part
                expression_part = calc_relation.formula_text.split('=')[1]
                expression = expression.replace(notation, '(' + expression_part + ')')
                pos = notations_to_replace.index(notation)
                del notations_to_replace[pos]
                notations_to_replace.extend(calc_relation.left_part)
                if expression_is_found(expression, notations, known_variables):
                    return expression
        except:
            pass
        
        return ''
        
def expression_is_found(expression, notations, known_variables):
    
    found = False
    if '=' in expression:
        expression_set = set(replace.met_notations(expression.split('=')[1], notations))
        known_set      = set(known_variables)
        if (expression_set.issuperset(known_set)):
            found = True
    return found

def get_solutions(soltree):
    
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
    solutions = map(lambda x: x[1:],steps)

    return solutions

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
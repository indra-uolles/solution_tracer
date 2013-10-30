# -*- coding: utf-8 -*-
'''
Created on 13.09.2013

@author: natalia

'''
import re

def get_replacements(notations):    
    initial_match_to = {}
    replaced_match_to = {}
    notations.sort(key=len, reverse=True)
    for j in range(0, len(notations)):
        initial_match_to[notations[j]] = 'x%sy' % str(j + 1)
        replaced_match_to['x%sy' % str(j + 1)] = notations[j]
    return (initial_match_to, replaced_match_to)
    
def get_transformed_expressions(expressions, notations):    
    transformed_expressions_list = []
    notations.sort(key=len, reverse=True)
    for e in expressions:
        transformed_expressions_list.append(replace_notations(e, notations))
    return transformed_expressions_list

def met_notations(expression, notations):
    notations.sort(key=len, reverse=True)
    expression = remove_operations_names(expression, notations)
    result = []
    for i in range(len(notations)):
        if (expression.find(notations[i]) != -1):
            result.append(notations[i])
            expression = expression.replace(notations[i], '')
    return result

def replace_notations_to_values(expression, notations, solution_point):    
    new_solution_point = {}
    expression = get_prepared_for_replacement(expression, notations)
    j = 0
    for i in range(len(notations)):
        j = j + 1
        var = 'x%sy' % j
        expression = expression.replace(notations[i], var) 
        new_solution_point['x%sy' % j] = solution_point[notations[i]]
        
    expression = get_postprocessed(expression)
    for k,v in new_solution_point.iteritems():
        replacement = str(v)
        if '-' in replacement:
            replacement = '(' + replacement + ')'
        expression = expression.replace(k, replacement)
        
    return expression

def replace_notations(expression, notations):    
    expression = get_prepared_for_replacement(expression, notations)

    j = 0
    for i in range(len(notations)):
        j = j + 1
        var = 'x%sy' % j
        expression = expression.replace(notations[i], var)  
        
    expression = get_postprocessed(expression)

    return expression   

def get_prepared_for_replacement(expression, notations):    
    #убираем все лишние пробелы
    expression = expression.strip(' \t\n')
    expression = expression.replace(' ', '')   
    
    #убираем sqrt
    reObj = re.compile(r'sqrt\{(.*?)\}')
    list_of_roots = reObj.findall(expression)
    for i in range(len(list_of_roots)):
        expression = expression.replace('sqrt{' + list_of_roots[i] + '}', '(' + list_of_roots[i] + ')**0.5')

    #убираем frac
    reObj = re.compile(r'frac\{(.*?)\}\{(.*?)\}')
    list_of_fracs = reObj.findall(expression)
    for i in range(len(list_of_fracs)):
        num = list_of_fracs[i][0]
        denum = list_of_fracs[i][1]
        expression = expression.replace('frac{' + num + '}{' + denum + '}', '(' + num + ')' + '/' + '(' + denum + ')')
    
    expression = remove_operations_names(expression, notations)
    
    return expression

def get_postprocessed(expression):    
    #умножение между переменной и переменной или скобкой
    expression = expression.replace('yx', 'y*x').replace('y(', 'y*(').replace(')x', ')*x')

    #умножение между цифрой и переменной или открывающейся скобкой
    r = re.compile(r'(\d)([x\(])')
    expression = r.sub(r'\1*\2', expression)
    expression = return_operations_names(expression)
    
    #возведение в степень
    expression = expression.replace("^","**")    
    
    return expression

def remove_operations_names(expression, notations):
    '''служебные слова временно заменяем на другие, чтобы не было пересечения по символам, а после обработки 
    по всем переменным, вернём обратно. Предполагается, что обозначения в своем названии не содержат фрагментов, 
    совпадающих с названием функций'''
    replacements_dict = get_operations_names_replacements()
    for key, value in replacements_dict.items():
        expression = expression.replace(value, key)
    return expression
    
def return_operations_names(expression):
    replacements_dict = get_operations_names_replacements()
    for key, value in replacements_dict.items():
        expression = expression.replace(key, value)
    return expression

def get_operations_names_replacements():
    return {'#1#' : 'Rational', '#2#' : 'Matrix', '#3#' : '#fixed#', '#4#' : '#almost#', '#5#' : 'sqrt', '#6#' : 'frac'}
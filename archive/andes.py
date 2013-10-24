# -*- coding: utf-8 -*-
'''
Created on 12.02.2013
@author: natalia
'''

from sympy import Symbol, Matrix, symbols
import numpy as np
import util
from common import replace
        
def calculate_dependencies(equations, task_variables, variables_values):
    
    replacements = replace.get_replacements(task_variables)[1]
    transformed_equations = replace.get_transformed_expressions(equations, task_variables)
    
    #prepare data for Numpy manipulations - change variables names to the names of special format - 'x%sy', also 
    #convert some strings to Symbols so they could be processed by Sympy and Numpy libs
        
    symbolized_replaced_task_variables = sorted(symbols(replacements.keys()))        
    replaced_variables_values = {}
    for k,v in replacements.iteritems():
        replaced_variables_values[Symbol(k)] = variables_values[v]
        
    #prepare the system of equations for solving - find Jacobian, in Jacobian matrix that was found replace variables by their values
    
    F = Matrix(transformed_equations)
    J = F.jacobian(symbolized_replaced_task_variables).evalf(subs=replaced_variables_values)
    X = np.transpose(np.array(J))
    
    #solve the system
    n,m = X.shape
    if (n != m - 1): 
        # if the system of equations is overdetermined (the number of equations is bigger than number of variables 
        #then we have to make regular, square systems of equations out of it (we do that by grabbing only some of the equations)
        square_systems = suggest_square_systems_list(X, n, m)
        for sq in square_systems:
            try:
                solve_system(sq, equations)
            except Exception as e:
                print e.args
                print sq
                
                
    else:
        solve_system(X, equations)  

def solve_system(G, equations):
    
    task_equations = G[:, :-1]
    student_equation = G[:, -1]       
    scalars = np.linalg.solve(task_equations, student_equation)
    print "Матрица: " 
    print G
    print "Ответ: "  
    print scalars
    Answer = "Для ввода формулы " + equations[len(equations)-1] + " студент использовал формулы "
    for i in range(len(scalars)):
        if scalars[i] != 0:
            Answer = Answer + equations[i] + ', '
    print Answer        
            
   
def suggest_square_systems_list(X, n, m):
    
    result = []   
    subsystems_indexes = util.SmartSublist(n-1, m-1, m-1).get_sublists()
    for i in range(len(subsystems_indexes)):
        F = []
        for j in range(len(subsystems_indexes[i])):
            F.append(X[subsystems_indexes[i][j], :]) 
        result.append(np.array(F))
            
    return result
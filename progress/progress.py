# -*- coding: utf-8 -*-
'''
Created on 15.02.2013

@author: natalia
'''
from common import util
from solutions import solbuild as sb, solget as sg

class ProgressCalculator(object):
    
    def __init__(self, calc_relations, notations, sought_variable, known_variables, solution_point):
        fp = util.FormulasPreprocessor(notations)
        self.calc_relations = fp.get_calc_relations(calc_relations)
        self.known_variables = fp.get_variables(known_variables)
        self.sought_variable = fp.get_variables([sought_variable])[0]   
                
        solutions = sg.get_solutions(
        sb.build_solutions_tree(self.calc_relations, self.sought_variable, self.known_variables))
        
        progress_rates = []
        for solution in solutions:
            progress_rates.append(ProgressRate(solution))    
        self.progress_rates = progress_rates  
        
        
class ProgressRate(object):
    
    def __init__(self, solution):
        self.solution = solution
        self.used = [False for x in range(len(solution))]    
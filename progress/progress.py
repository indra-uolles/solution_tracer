# -*- coding: utf-8 -*-
'''
Created on 15.02.2013

@author: natalia
'''
from common import util, replace
from solutions import solbuild as sb, solget as sg

class ProgressCalculator(object):
    
    def __init__(self, calc_relations, notations, sought_variable, known_variables, solution_point):
        fp = util.FormulasPreprocessor(notations)
        self.calc_relations = fp.get_calc_relations(calc_relations)
        self.known_variables = fp.get_variables(known_variables)
        self.sought_variable = fp.get_variables([sought_variable])[0]   
        self.notations = notations
        self.solution_point = fp.get_solution_point(solution_point)
                
        soltree = sb.build_solutions_tree(self.calc_relations, self.sought_variable, self.known_variables, [])
        solutions = sg.get_solutions(soltree.get_data(), self.calc_relations)
        
        progress_rates = []
        for solution in solutions:
            progress_rates.append(ProgressRate(solution))    
        self.progress_rates = progress_rates 
        
    def update(self, student_formula): 
        def update_progress_rates(calc_ids):
            for pr in self.progress_rates:
                solution = pr.get_solution()
                used_calc_ids = pr.get_used_calc_ids()
                solution_ids = solution.get_calc_ids()
                for calc_id in calc_ids:
                    if calc_id in solution_ids:
                        pos = solution_ids.index(calc_id)
                        used_calc_ids[pos] = True
                pr.set_used_calc_ids(used_calc_ids)
            
        fp                          = util.FormulasPreprocessor(self.notations)
        formula_left, formula_right = student_formula.split('=')
        sought_variable             = replace.met_notations(formula_left, self.notations)
        variables                   = replace.met_notations(formula_right, self.notations)
        sought_variable             = fp.get_variables(sought_variable)[0] 
        variables                   = fp.get_variables(variables)
        solutions                   = self.get_solutions()
        student_formula             = replace.replace_notations(student_formula, self.notations)
        notations                   = fp.get_variables(self.notations)
        
        system_expressions = sg.construct_system_expressions(self.calc_relations, notations, solutions, sought_variable, variables)
        if (sg.is_correct(student_formula, system_expressions, self.notations, self.solution_point)):
            for x in system_expressions:
                calc_ids = x.get_calc_ids()
                update_progress_rates(calc_ids)
                
    def get_progress(self):
        max_progress = 0
        for pr in self.progress_rates:
            used_calc_ids = pr.get_used_calc_ids()
            used_amount = len(filter(lambda x: x== True, used_calc_ids))
            progress = used_amount*1.0 / len(used_calc_ids)
            if progress > max_progress:
                max_progress = progress
        return max_progress
        
    def get_solutions(self):
        solutions = map(lambda x: x.get_solution(), self.progress_rates)
        return solutions        
        
class ProgressRate(object):
    
    def __init__(self, solution):
        self.solution = solution
        self.used = [False for x in range(solution.length())]  
        
    def get_solution(self):  
        return self.solution
    
    def get_used_calc_ids(self):
        return self.used
    
    def set_used_calc_ids(self, used):
        self.used = used
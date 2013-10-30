# -*- coding: utf-8 -*-
'''
Created on 16.09.2013

@author: natalia
'''
import unittest
from common import replace
from solutions import calc
from solutions import solbuild as sb, solget as sg
from progress import progress

class Test(unittest.TestCase):


    def testName(self):
        
        #enter info about "basic" formulas for solutions generation and checking students' input
        calc_relations = []
        calc_relations.append(calc.CalcRelation('|c|',['p(a,b)'], 'p(a,b)=|c|')) 
        calc_relations.append(calc.CalcRelation('p(a,b)', ['|c|'], 'p(a,b)=|c|'))       
        calc_relations.append(calc.CalcRelation('|c|', ['(c,c)'], '|c|=sqrt{(c,c)}')) 
        calc_relations.append(calc.CalcRelation('(c,c)', ['|c|'], '|c|=sqrt{(c,c)}')) 
        calc_relations.append(calc.CalcRelation('(c,c)', ['c_1','c_2'], '(c,c)=c_1^2+c_2^2'))        
        calc_relations.append(calc.CalcRelation('c', ['a','b'], 'c=a-b'))       
        calc_relations.append(calc.CalcRelation('c', ['c_1', 'c_2'], 'c=[c_1;c_2]')) 
        calc_relations.append(calc.CalcRelation('a', ['a_1', 'a_2'], 'a=[a_1;a_2]'))       
        calc_relations.append(calc.CalcRelation('b', ['b_1', 'b_2'], 'b=[b_1;b_2]')) 
        calc_relations.append(calc.CalcRelation('c_1', ['a_1', 'b_1'], 'c_1=a_1-b_1')) 
        calc_relations.append(calc.CalcRelation('c_2', ['a_2', 'b_2'], 'c_2=a_2-b_2')) 
        calc_relations.append(calc.CalcRelation('(c,c)', ['c'], 'по с можно вычислить (c,c)')) 
        notations = ['a', 'a_1', 'a_2', 'a_3', 'a_4', 'b', 'b_1', 'b_2', 'b_3', 'b_4', 'p(a,b)', 'c', 'c_1', 'c_2', 'c_3', 'c_4', '|c|', '(c,c)']
        solution_point = {'a_1': 1, 'b_1': 3, 'a_2': 2, 'b_2': 4, 'c_1': -2, 'c_2': -2, '(c,c)': 8}
                         
        #build solutions tree 
        soltree = sb.build_solutions_tree(calc_relations, 'p(a,b)', ['a_1', 'a_2', 'b_1', 'b_2'])   
        self.assertItemsEqual(soltree, {0: [[1]], 1: [[2]], 2: [[4], [11]], 4: [[9, 10]], 5: [[7, 8]], 6: [[9, 10]], 11: [[5], [6]]}, 
        u"Тест 1 не пройден") 
             
        #get solutions from solutions tree
        solution1 = sg.Solution([1, 2, 4, 9, 10], ['p(a,b)', '|c|', '(c,c)', 'c_1', 'c_2'])
        solution2 = sg.Solution([1, 2, 11, 5, 7, 8], ['p(a,b)', '|c|', '(c,c)', 'c', 'a', 'b'])
        solution3 = sg.Solution([1, 2, 11, 6, 9, 10], ['p(a,b)', '|c|', '(c,c)', 'c', 'c_1', 'c_2'])
        solutions = [solution1, solution2, solution3]
        tested = sg.get_solutions(soltree, calc_relations)
        self.assertEquals(len(solutions), len(tested), u"Тест 2 не пройден (длины списков не совпадают)") 
        for i in range(len(solutions)):
            self.assertItemsEqual(solutions[i].get_calc_ids(), tested[i].get_calc_ids(), 
            u"Тест 2 не пройден (не совпадают списки id отношений вычислимости)")
            self.assertItemsEqual(solutions[i].get_goal_variables(), tested[i].get_goal_variables(), 
            u"Тест 2 не пройден (не совпадают списки целевых величин)") 
            
        #construct formula from the specified part of a solution - 1
        expression = sg.SystemExpression('(c,c)=c_1^2+c_2^2', [4])
        tested = sg.construct_system_expressions(calc_relations, notations, solutions, '(c,c)', ['c_1', 'c_2'])
        self.assertEquals(tested[0].get_expression(), expression.get_expression(), u"Тест 3.1 не пройден (не совпадают выражения)")
        self.assertItemsEqual(tested[0].get_calc_ids(), expression.get_calc_ids(), u"Тест 3.1 не пройден(не совпадают списки id отношений вычислимости)")
        
        #construct formula from the specified part of a solution - 2
        expression = sg.SystemExpression('(c,c)=(a_1-b_1)^2+c_2^2', [4,9])
        tested = sg.construct_system_expressions(calc_relations, notations, solutions, '(c,c)', ['a_1', 'b_1'])
        self.assertEquals(tested[0].get_expression(), expression.get_expression(), u"Тест 3.2 не пройден (не совпадают выражения)")
        self.assertItemsEqual(tested[0].get_calc_ids(), expression.get_calc_ids(), u"Тест 3.2 не пройден(не совпадают списки id отношений вычислимости)")
     
        #simple check of student formula
        self.assertEqual(replace.replace_notations_to_values('(c,c)=(a_1-b_1)^2+(a_2-b_2)^2', 
			replace.met_notations('(c,c)=(a_1-b_1)^2+(a_2-b_2)^2', notations), solution_point), '8=(1-3)**2+(2-4)**2', u"Тест 4 не пройден")
         
        #check if student's step is correct and is not an imitation - 1 (student's step is correct)
        student_formula = '(c,c)=(a_1-b_1)^2+4'
        formula_left, formula_right = student_formula.split('=')
        sought_variable  = replace.met_notations(formula_left, notations)[0]
        variables = replace.met_notations(formula_right, notations)
        system_expressions = sg.construct_system_expressions(calc_relations, notations, solutions, sought_variable, variables)
        self.assertEqual(True, sg.is_correct(student_formula, system_expressions, notations, solution_point),
			u"Тест 5 не пройден")
         
        #check if student's step is correct and is not an imitation - 2 (student's step is imitation)
        student_formula = '(c,c)=c_1+c_2+12'
        formula_left, formula_right = student_formula.split('=')
        sought_variable  = replace.met_notations(formula_left, notations)[0]
        variables = replace.met_notations(formula_right, notations)
        system_expressions = sg.construct_system_expressions(calc_relations, notations, solutions, sought_variable, variables)
        self.assertEqual(False, sg.is_correct(student_formula, system_expressions, notations, solution_point),
			u"Тест 6 не пройден")  
         
        #check if student's step is correct and is not an imitation - 3 (student's step is correct)
        student_formula = '(c,c)=c_1^2+c_2^2'
        formula_left, formula_right = student_formula.split('=')
        sought_variable  = replace.met_notations(formula_left, notations)[0]
        variables = replace.met_notations(formula_right, notations)
        system_expressions = sg.construct_system_expressions(calc_relations, notations, solutions, sought_variable, variables)
        self.assertEqual(True, sg.is_correct(student_formula, system_expressions, notations, solution_point),
			u"Тест 7 не пройден")    
        
        #test progress calculator
        prc =  progress.ProgressCalculator(calc_relations, notations, 'p(a,b)', ['a_1', 'a_2', 'b_1', 'b_2'], solution_point)
        student_formula = '(c,c)=c_1^2+c_2^2'
        prc.update(student_formula)
        self.assertEqual(0.2, prc.get_progress(), u"Тест 8 не пройден")    
        
        student_formula = '(c,c)=(a_1-b_1)^2+(a_2-b_2)^2'
        prc.update(student_formula)
        self.assertEqual(0.6, prc.get_progress(), u"Тест 9 не пройден")    
   
        
if __name__ == "__main__":
    unittest.main()
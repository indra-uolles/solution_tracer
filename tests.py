# -*- coding: utf-8 -*-
'''
Created on 16.09.2013

@author: natalia
'''
import unittest
from common import replace, equiv
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
        notations = ['a', 'a_1', 'a_2', 'a_3', 'a_4', 'b', 'b_1', 'b_2', 'b_3', 'b_4', 'p(a,b)', 'c', 'c_1', 'c_2', 'c_3', 'c_4', '|c|', '(c,c)']
        solution_point = {'a_1': 1, 'b_1': 3, 'a_2': 2, 'b_2': 4, 'c_1': -2, 'c_2': -2, '(c,c)': 8}
        vectors = ['c', 'a', 'b']
        sought_variable = 'p(a,b)'
        known_variables = ['a_1', 'a_2', 'b_1', 'b_2']
                         
        #build solutions tree 
        soltree, requirements = sb.build_solutions_tree_requirements(calc_relations, sought_variable, known_variables, vectors)   
        self.assertItemsEqual(soltree.get_data(), {0: [[1]], 1: [[2]], 2: [[4]]}, 
        u"Тест 1.1 не пройден") 
        self.assertEqual(len(requirements), 1, u"Тест 1.2 не пройден")
        self.assertEqual(requirements[0].get_required(), 'c', u"Тест 1.2 не пройден")
        self.assertEqual(requirements[0].get_initiators_set(), set(['c_1', 'c_2']), u"Тест 1.2 не пройден")
        
        soltree2, requirements2 = sb.build_solutions_tree_requirements(calc_relations, 'c', known_variables, vectors, requirements[0].get_initiators_set())
        self.assertItemsEqual(soltree2.get_data(), {0: [[5]], 5: [[7, 8]]}, 
        u"Тест 1.3 не пройден") 
        self.assertEqual(requirements2, [], u"Тест 1.4 не пройден")
             
        #get solutions from solutions tree
        solutions1 = [sg.Solution([1, 2, 4], ['p(a,b)', '|c|', '(c,c)'])]
        tested = sg.get_solutions(soltree.get_data(), calc_relations)
        self.assertEquals(len(solutions1), len(tested), u"Тест 2 не пройден (длины списков не совпадают)") 
        for i in range(len(solutions1)):
            self.assertItemsEqual(solutions1[i].get_calc_ids(), tested[i].get_calc_ids(), 
            u"Тест 2 не пройден (не совпадают списки id отношений вычислимости)")
            self.assertItemsEqual(solutions1[i].get_goal_variables(), tested[i].get_goal_variables(), 
            u"Тест 2 не пройден (не совпадают списки целевых величин)") 
            
        solutions2 = [sg.Solution([5, 7, 8], ['c', 'a', 'b'])]
        tested2 = sg.get_solutions(soltree2.get_data(), calc_relations)
        self.assertEquals(len(solutions2), len(tested), u"Тест 2 не пройден (длины списков не совпадают)") 
        for i in range(len(solutions2)):
            self.assertItemsEqual(solutions2[i].get_calc_ids(), tested2[i].get_calc_ids(), 
            u"Тест 2 не пройден (не совпадают списки id отношений вычислимости)")
            self.assertItemsEqual(solutions2[i].get_goal_variables(), tested2[i].get_goal_variables(), 
            u"Тест 2 не пройден (не совпадают списки целевых величин)")
            
        #match vector coordinates
        vector_expression1 = '([a_1;a_2])-([b_1;b_2])'
        vector_expression2 = '([c_1;c_2])'
        matches = equiv.match_vector_coordinates(notations, vector_expression1, vector_expression2)
        self.assertItemsEqual(matches, {'c_1': 'a_1 - b_1', 'c_2': 'a_2 - b_2'}, u"Тест 3 не пройден")
             
        #construct formula from the specified part of a solution - 1
        solutions_groups = [solutions1, solutions2]
        expression = sg.SystemExpression('(c,c)=c_1^2+c_2^2', [4])
        tested = sg.construct_system_expressions(calc_relations, notations, solutions_groups, '(c,c)', ['c_1', 'c_2'], vectors)
        self.assertEquals(tested[0].get_expression(), expression.get_expression(), u"Тест 3.1 не пройден (не совпадают выражения)")
        self.assertItemsEqual(tested[0].get_calc_ids(), expression.get_calc_ids(), u"Тест 3.1 не пройден(не совпадают списки id отношений вычислимости)")
        
        #construct formula from the specified part of a solution - 2
        expression = sg.SystemExpression('(c,c)=(a_1 - b_1)^2+(a_2 - b_2)^2', [4,5,7,8])
        #TO DO: there can also be cases like that: '(c,c)=(a_1-b_1)^2+c_2^2'
        tested = sg.construct_system_expressions(calc_relations, notations, solutions_groups, '(c,c)', ['a_1', 'b_1', 'a_2', 'b_2'], vectors)
        self.assertEquals(tested[0].get_expression(), expression.get_expression(), u"Тест 3.2 не пройден (не совпадают выражения)")
        self.assertItemsEqual(tested[0].get_calc_ids(), expression.get_calc_ids(), u"Тест 3.2 не пройден(не совпадают списки id отношений вычислимости)")
      
        #simple check of student formula
        self.assertEqual(replace.replace_notations_to_values('(c,c)=(a_1-b_1)^2+(a_2-b_2)^2', 
			replace.met_notations('(c,c)=(a_1-b_1)^2+(a_2-b_2)^2', notations), solution_point), '8=(1-3)**2+(2-4)**2', u"Тест 4 не пройден")
#          
#         #check if student's step is correct and is not an imitation - 1 (student's step is correct)
#         student_formula = '(c,c)=(a_1-b_1)^2+4'
#         formula_left, formula_right = student_formula.split('=')
#         sought_variable  = replace.met_notations(formula_left, notations)[0]
#         variables = replace.met_notations(formula_right, notations)
#         system_expressions = sg.construct_system_expressions(calc_relations, notations, solutions, sought_variable, variables)
#         self.assertEqual(True, sg.is_correct(student_formula, system_expressions, notations, solution_point),
# 			u"Тест 5 не пройден")
#          
#         #check if student's step is correct and is not an imitation - 2 (student's step is imitation)
#         student_formula = '(c,c)=c_1+c_2+12'
#         formula_left, formula_right = student_formula.split('=')
#         sought_variable  = replace.met_notations(formula_left, notations)[0]
#         variables = replace.met_notations(formula_right, notations)
#         system_expressions = sg.construct_system_expressions(calc_relations, notations, solutions, sought_variable, variables)
#         self.assertEqual(False, sg.is_correct(student_formula, system_expressions, notations, solution_point),
# 			u"Тест 6 не пройден")  
#          
#         #check if student's step is correct and is not an imitation - 3 (student's step is correct)
#         student_formula = '(c,c)=c_1^2+c_2^2'
#         formula_left, formula_right = student_formula.split('=')
#         sought_variable  = replace.met_notations(formula_left, notations)[0]
#         variables = replace.met_notations(formula_right, notations)
#         system_expressions = sg.construct_system_expressions(calc_relations, notations, solutions, sought_variable, variables)
#         self.assertEqual(True, sg.is_correct(student_formula, system_expressions, notations, solution_point),
# 			u"Тест 7 не пройден")    
#         
#         #test progress calculator
#         prc =  progress.ProgressCalculator(calc_relations, notations, 'p(a,b)', ['a_1', 'a_2', 'b_1', 'b_2'], solution_point)
#         student_formula = '(c,c)=c_1^2+c_2^2'
#         prc.update(student_formula)
#         self.assertEqual(0.2, prc.get_progress(), u"Тест 8 не пройден")    
#         
#         student_formula = '(c,c)=(a_1-b_1)^2+(a_2-b_2)^2'
#         prc.update(student_formula)
#         self.assertEqual(0.6, prc.get_progress(), u"Тест 9 не пройден")   
#    
        
if __name__ == "__main__":
    unittest.main()
# -*- coding: utf-8 -*-
'''
Created on 16.09.2013

@author: natalia
'''
import unittest
from common import replace
from solutions import calc
from solutions import solbuild as sb, solget as sg

class Test(unittest.TestCase):


    def testName(self):
        
        notations = ['a', 'a_1', 'a_2', 'a_3', 'a_4', 'b', 'b_1', 'b_2', 'b_3', 'b_4', 'p(a,b)', 'c', 'c_1', 'c_2', 'c_3', 'c_4', '|c|', '(c,c)']
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
          
        #Test solutions tree                 
                
        soltree = sb.build_solutions_tree(calc_relations, 'p(a,b)', ['a_1', 'a_2', 'b_1', 'b_2'])   
        self.assertItemsEqual(soltree, {0: [[1]], 1: [[2]], 2: [[4], [11]], 4: [[9, 10]], 5: [[7, 8]], 6: [[9, 10]], 11: [[5], [6]]}, 
        u"Тест 1 не пройден") 
           
        soltree = sb.build_solutions_tree(calc_relations, '(c,c)', ['a_1', 'a_2', 'b_1', 'b_2'])
        self.assertItemsEqual(sg.get_solutions(soltree), [[4, 9, 10], [11, 5, 7, 8], [11, 6, 9, 10]], u"Тест 2 не пройден") 
          
        #надо доделать, пока не работает
        #soltree = sb.build_solutions_tree(calc_relations, '(c,c)', ['c_1', 'c_2'])  
        #self.assertItemsEqual(['(c,c)=c_1^2+c_2^2'], sg.form_expressions(sg.get_solutions(sb.build_solutions_tree(calc_relations, 
        #'(c,c)', ['с_1', 'с_2'])), calc_relations, notations, ['c_1', 'c_2']), u"Тест 3 не пройден")
        #self.assertEqual(True, heuristics.is_imitation('(c,c)=c_1+c_2+12', 
        #sg.form_expressions(sg.get_solutions(sb.build_solutions_tree(calc_relations, 
        #notations, '(c,c)=c_1+c_2+12', ['a_1', 'a_2', 'b_1', 'b_2'])), calc_relations, notations, ['a_1', 'a_2', 'b_1', 'b_2']), notations, solution_point),
        #u"Тест 9 не пройден")         
        #system_expressions = sg.form_expressions(sg.get_solutions(sb.build_solutions_tree(calc_relations, 
        #notations, '(c,c)=(a_1-b_1)^2+4', ['a_1', 'a_2', 'b_1', 'b_2'])), calc_relations, notations, ['a_1', 'a_2', 'b_1', 'b_2'])
        #self.assertEqual(False, heuristics.is_imitation('(c,c)=(a_1-b_1)^2+4', system_expressions, notations, solution_point), u"Тест 10 не пройден")
          
        solution_point = {'a_1': 1, 'b_1': 3, 'a_2': 2, 'b_2': 4, 'c_1': -2, 'c_2': -2, '(c,c)': 8}
        self.assertEqual(replace.replace_notations_to_values('(c,c)=(a_1-b_1)^2+(a_2-b_2)^2', ['a_1', 'b_1', 'a_2', 'b_2', '(c,c)'], solution_point), '8=(1-3)^2+(2-4)^2', u"Тест 8 не пройден")
   
        
if __name__ == "__main__":
    unittest.main()
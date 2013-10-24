# -*- coding: utf-8 -*-
'''
Created on 16.09.2013

@author: natalia
'''
import unittest
from common import replace
from solutions import calc
import my_method
import deps

class Test(unittest.TestCase):


    def testName(self):
               
        #Test replace
        expressions = ['Fw_x - Fw*cos(250)', 'Fw - mc*g', 'mc - 2000', 'g - 9.8', 'Fw_x + mc*g*sin(20)']
        notations = ['Fw_x', 'Fw', 'mc', 'g']
        initial_match_to, replaced_match_to = replace.get_replacements(notations)
        transformed_expressions = replace.get_transformed_expressions(expressions, notations)
        self.assertEqual(initial_match_to, {'Fw_x' : 'x1y', 'Fw' : 'x2y', 'mc' : 'x3y', 'g' : 'x4y'}, u"Тест 1 не пройден") 
        self.assertEqual(replaced_match_to, {'x1y' : 'Fw_x', 'x2y' : 'Fw', 'x3y' : 'mc', 'x4y' : 'g'}, u"Тест 1 не пройден")   
        self.assertEqual(transformed_expressions, ['x1y-x2y*cos(250)', 'x2y-x3y*x4y', 'x3y-2000', 'x4y-9.8', 'x1y+x3y*x4y*sin(20)'], u"Тест 1 не пройден")
        self.assertEqual(replace.met_notations('Fw_x + mc*g*sin(20)', notations), ['Fw_x', 'mc', 'g'], u"Тест 1 не пройден")

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
        
        #Первая версия алгоритма выявления зависимостей между формулой, введенной студентом и "базовыми" формулами задачи
        self.assertEqual(my_method.show_dependencies(calc_relations, notations, 'p(a,b)=sqrt{(c,c)}')[0], 'формула студента p(a,b)=sqrt{(c,c)} получена комбинацией формул:|c|=sqrt{(c,c)}, p(a,b)=|c|', u"Тест 2-0 не пройден")
        self.assertEqual(my_method.show_dependencies(calc_relations, notations, 'p(a,b)=sqrt{(a_1-b_1)**2+(a_2-b_2)**2}')[0], 
        'формула студента p(a,b)=sqrt{(a_1-b_1)**2+(a_2-b_2)**2} получена комбинацией формул:b=[b_1;b_2], a=[a_1;a_2], c=a-b, по с можно вычислить (c,c), |c|=sqrt{(c,c)}, p(a,b)=|c|', 
        u"Тест 2-1 не пройден")
        self.assertEqual(my_method.show_dependencies(calc_relations, notations, 'p(a,b)=sqrt{(a_1-b_1)**2+(a_2-b_2)**2}')[1], 
        'формула студента p(a,b)=sqrt{(a_1-b_1)**2+(a_2-b_2)**2} получена комбинацией формул:c_1=a_1-b_1, c_2=a_2-b_2, (c,c)=c_1^2+c_2^2, |c|=sqrt{(c,c)}, p(a,b)=|c|', 
        u"Тест 2-2 не пройден")
        self.assertEqual(my_method.show_dependencies(calc_relations, notations, 'p(a,b)=sqrt{(a_1-b_1)**2+(a_2-b_2)**2}')[2], 
        'формула студента p(a,b)=sqrt{(a_1-b_1)**2+(a_2-b_2)**2} получена комбинацией формул:b=[b_1;b_2], a=[a_1;a_2], c=a-b, по с можно вычислить (c,c), |c|=sqrt{(c,c)}, p(a,b)=|c|', 
        u"Тест 2-3 не пройден")
        
        #Вторая версия алгоритма выявления зависимостей между формулой, введенной студентом и "базовыми" формулами задачи
        self.assertEqual(deps.show_dependencies(calc_relations, notations, 'p(a,b)=sqrt{(c,c)}')[0], 'формула студента p(a,b)=sqrt{(c,c)} получена комбинацией формул:|c|=sqrt{(c,c)}, p(a,b)=|c|', u"Тест 2-0 не пройден")
        self.assertEqual(deps.show_dependencies(calc_relations, notations, 'p(a,b)=sqrt{(a_1-b_1)**2+(a_2-b_2)**2}')[0], 
        'формула студента p(a,b)=sqrt{(a_1-b_1)**2+(a_2-b_2)**2} получена комбинацией формул:b=[b_1;b_2], a=[a_1;a_2], c=a-b, по с можно вычислить (c,c), |c|=sqrt{(c,c)}, p(a,b)=|c|', 
        u"Тест 2-1 не пройден")
        self.assertEqual(deps.show_dependencies(calc_relations, notations, 'p(a,b)=sqrt{(a_1-b_1)**2+(a_2-b_2)**2}')[1], 
        'формула студента p(a,b)=sqrt{(a_1-b_1)**2+(a_2-b_2)**2} получена комбинацией формул:c_1=a_1-b_1, c_2=a_2-b_2, (c,c)=c_1^2+c_2^2, |c|=sqrt{(c,c)}, p(a,b)=|c|', 
        u"Тест 2-2 не пройден")
        self.assertEqual(deps.show_dependencies(calc_relations, notations, 'p(a,b)=sqrt{(a_1-b_1)**2+(a_2-b_2)**2}')[2], 
        'формула студента p(a,b)=sqrt{(a_1-b_1)**2+(a_2-b_2)**2} получена комбинацией формул:b=[b_1;b_2], a=[a_1;a_2], c=a-b, по с можно вычислить (c,c), |c|=sqrt{(c,c)}, p(a,b)=|c|', 
        u"Тест 2-3 не пройден")       
        

if __name__ == "__main__":
    unittest.main()
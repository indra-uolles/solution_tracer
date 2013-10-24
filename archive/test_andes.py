# -*- coding: utf-8 -*-
'''
Created on 12.02.2013

@author: natalia
'''
import unittest
import andes
import util

class Test(unittest.TestCase):

    def testName(self):
        
        #Test get subsets of certain length - we define the lower and upper bound for the lengths of subsets
        self.assertEqual(util.SmartSublist(4, 2, 2).get_sublists(), [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)], u"Тест 0 не пройден")
        self.assertEqual(util.SmartSublist(4, 2, 4).get_sublists(), [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3), (0, 1, 2, 3)], u"Тест 0 не пройден")

        #Tecт 1
        #считается, что уравнение, введенное студентом, находится последним
        equations = ['Fw_x - Fw*cos(250)', 'Fw - mc*g', 'mc - 2000', 'g - 9.8', 'Fw_x + mc*g*sin(20)']
        task_variables = ['Fw_x', 'Fw', 'mc', 'g']
        variables_values = {'Fw_x' : -6703.5948, 'mc' : 2000, 'g' : 9.8, 'Fw' : 19600}
        andes.calculate_dependencies(equations, task_variables, variables_values)
        
        #Тест 2
        equations = ['p(a,b)-|c|', 'c_1 - a_1 + b_1 ', 'c_2 - a_2 + b_2', '|c| - sqrt{(c,c)}', '(c,c) - c_1^2 - c_2^2', 'p(a,b) - sqrt{(c,c)}']
        task_variables = ['p(a,b)', '|c|', 'c_1', 'a_1', 'b_1', 'c_2', 'a_2', 'b_2', '(c,c)']
        variables_values = {'p(a,b)' : 8**0.5, '|c|' : 8**0.5, 'c_1' : -2, 'c_2' : -2, 'a_1' : 1, 'a_2' : 2, 'b_1' : 3, 'b_2' : 4, '(c,c)' : 8}
        andes.calculate_dependencies(equations, task_variables, variables_values)

if __name__ == "__main__":
    unittest.main()
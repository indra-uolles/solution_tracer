# -*- coding: utf-8 -*-
'''
Created on 05.10.2013

@author: natalia, a.abramenkov

'''
import re
from sympy import simplify
from sympy.core import Symbol
from sympy.core.numbers import Float

def check_expression (pattern, expression):
    '''
    Сравниваем два выражения не содержащих равенство, например 2*(a+b) и 2*b+2*a.
    Замечание: simplify для матриц работает не так как для обычных строк, в частности, не упрощает сложные выражения
    '''

    dif = Symbol('dif')
    try:
        dif = simplify(pattern + '- (' + expression + ')')
    except:
        return 0
    #если результат матрица
    #todo: округление для матриц
    try:
        if(dif.is_Matrix):
            #проверка на то, что матрица нулевая, не нашёл стандартного способа
            r = re.compile(r'[\s\[\],0]')
            res = r.sub('', '%s' % dif)
            if(res == ''):
                return 1            
            return 0
    except:
        pass
    #округление для случая небольшого несоответствия
    accuracy = 2
    dif = simplify(dif.subs([(n, round(n, accuracy)) for n in dif.atoms(Float)]))
    if(dif == 0):
        return 1
    else:
        #это для случаев, когда студент может ввести как \sqrt{66}, так и 8.128, округление выше в этих случаях не работает
        try:
            if (abs(round(dif,2))==0):
                return 1  
        except:
            return 0                 
    return 0
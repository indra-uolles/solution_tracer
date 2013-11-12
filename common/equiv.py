# -*- coding: utf-8 -*-
'''
Created on 05.10.2013

@author: natalia, a.abramenkov

'''
import re
from sympy import simplify
from sympy.core import Symbol
from sympy.core.numbers import Float
from common import replace
from sympy.unify.usympy import unify
from sympy import symbols

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

def match_vector_coordinates(notations, vector_expression1, vector_expression2):
    variables_names = replace.met_notations(vector_expression1, notations) + replace.met_notations(vector_expression2, notations)
    variables = []
    for var_name in variables_names:
        locals()[var_name] = Symbol(var_name) 
        variables.append(locals()[var_name])
    variables = tuple(variables)
    vector_expression1 = preprocess_vector_expression_for_unify(vector_expression1)
    vector_expression2 = preprocess_vector_expression_for_unify(vector_expression2)
    matches = next(unify(vector_expression1, vector_expression2, {}, variables))
    return get_postprocessed_matches(matches)

def preprocess_vector_expression_for_unify(vector_expression):
    reObj = re.compile(r'(\(\[[^\[\]]+[;]+[^\[\]]+\]\))') 
    #if expression is ([a_1;a_2])-([b_1;b_2]), it will find ([a_1;a_2]) and ([b_1;b_2])
    vectors = reObj.findall(vector_expression)
    for v in vectors:
        new_v = 'ImmutableMatrix' + v
        new_v = new_v.replace(';', ',')
        vector_expression = vector_expression.replace(v, new_v)
    return simplify(vector_expression)

def get_postprocessed_matches(matches):
    new_matches = {}
    for k,v in matches.iteritems():
        new_matches[str(k)]=str(v)
    return new_matches
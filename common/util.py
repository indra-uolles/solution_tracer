# -*- coding: utf-8 -*-
'''
Created on 18.09.2013

@author: natalia
'''
import copy
import replace

class FormulasPreprocessor(object):

    def __init__(self, notations):
        self.replacements = replace.get_replacements(notations)[0]
        self.notations = notations
    
    def get_variables(self, variables):
        return map(lambda x: replace.replace_notations(x, self.notations), variables)
    
    def get_calc_relations(self, calc_relations):
        _calc_relations = copy.deepcopy(calc_relations)
        for element in _calc_relations:
            element.right_part=self.replacements[element.right_part]
            element.left_part = map(lambda x: self.replacements[x], element.left_part)
        return _calc_relations               
    
def get_calc_relation_by_id(_calc_relations, selected_id):

    for cr in _calc_relations:
        if (cr.get_id() == selected_id):
            return cr
    raise LookupError 
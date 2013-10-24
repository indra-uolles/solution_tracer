# -*- coding: utf-8 -*-
'''
Created on 15.02.2013

@author: natalia
'''
import itertools

class CalcRelation(object):
    '''
    classdocs
    '''
    new_id = itertools.count().next

    def __init__(self, right_part, left_part, formula_text):
        '''
        Constructor
        '''

        self.id           = CalcRelation.new_id()
        self.right_part   = right_part        
        self.left_part    = left_part
        self.formula_text = formula_text
        
    def get_id(self):
        return self.id   
        
class Path(object):
    '''
    classdocs
    '''
    new_id = itertools.count().next

    def __init__(self, new_notation, ignorelist, indexes, chosen_id=-1):
        '''
        Constructor
        '''
        if chosen_id == - 1:
            self.id       = Path.new_id()   
        else:
            self.id       = chosen_id
        self.new_notation = new_notation
        self.ignorelist   = ignorelist
        self.indexes      = indexes
        self.found        = False
        
    def check_if_found(self, goal_notation):
        if self.new_notation[0] == goal_notation:
            self.found = True
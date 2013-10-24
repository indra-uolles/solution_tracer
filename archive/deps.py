# -*- coding: utf-8 -*-
'''
Created on 14.02.2013

@author: natalia
'''
import copy
from common import replace
from solutions import calc
import util

def show_dependencies(calc_relations, notations, student_formula):
    
    dependencies = calculate_dependencies(calc_relations, notations, student_formula)
    return show_answer(calc_relations, dependencies, student_formula)    
       
def calculate_dependencies(calc_relations, notations, student_formula):
    
    dependencies = [] 
    _calc_relations, student_leftmost_notations, student_rightmost_notations = get_preprocessed_relations_and_notations(calc_relations, student_formula, notations)   
    solution_paths = get_possible_solution_paths(_calc_relations, student_leftmost_notations, calc.Path(student_rightmost_notations, student_rightmost_notations, []))
    
    if (len(solution_paths) == 0):
        solution_paths = get_new_paths_by_combining_calc_relations(_calc_relations, student_rightmost_notations)
            
    while (len(solution_paths) > 0):
        new_dependencies = get_dependencies_from_paths(_calc_relations, solution_paths)        
        if (len(new_dependencies) > 0):
            dependencies.extend(new_dependencies)
            new_solution_paths = get_filtered_solution_paths(solution_paths)
        else:  
            new_solution_paths = get_new_paths_by_expanding_existing_paths(_calc_relations, solution_paths, student_leftmost_notations)  
            #if (len(new_solution_paths) == 0):   TO DO: add code when we get necessary test cases         
        solution_paths = get_updated_solution_paths(new_solution_paths)                                       
 
    return dependencies
   
def get_preprocessed_relations_and_notations(calc_relations, student_formula, notations):
  
    _calc_relations = copy.deepcopy(calc_relations)
    
    #replace notations in knowledge base and in student's formula by notations safe for Sympy and Numpy (they look like that: x1y, x2y, etc.)
    replacements = replace.get_replacements(notations)[0]
     
    for element in _calc_relations:
        element.right_part=replacements[element.right_part]
        element.left_part = map(lambda x: replacements[x], element.left_part)

    #get notations from the left part and right part of student's formula (`=` divides student's formula into 2 parts)         
    student_leftmost_notations  = replace.met_notations(student_formula.split('=')[0], notations)
    student_leftmost_notations  = map(lambda x: replacements[x], student_leftmost_notations)
    student_rightmost_notations = replace.met_notations(student_formula.split('=')[1], notations)    
    student_rightmost_notations = map(lambda x: replacements[x], student_rightmost_notations)

    return _calc_relations, student_leftmost_notations, student_rightmost_notations 
   
def get_possible_solution_paths(_calc_relations, student_leftmost_notations, path):
 
    possible_solution_paths = []       
    for _cr in _calc_relations:
        if (not(_cr.right_part in path.ignorelist) and len(filter(lambda x: x in path.new_notation, _cr.left_part)) == len(path.new_notation)):
                path = calc.Path([_cr.right_part], path.ignorelist + path.new_notation, path.indexes + [_calc_relations.index(_cr)])
                #NB! we suggest that left part of student's formula consists of only one notation. 
                path.check_if_found(student_leftmost_notations[0])
                possible_solution_paths.append(path)
 
    return possible_solution_paths  
   
def get_new_paths_by_combining_calc_relations(_calc_relations, student_rightmost_notations): 

    solution_paths = []
    filtered_calc_relations = get_relations_intersecting_with_student_rightmost_notations(_calc_relations, student_rightmost_notations)
  
    _calc_sublists = util.SmartSublist(len(filtered_calc_relations), 2, len(filtered_calc_relations), filtered_calc_relations).get_sublists()
    _calc_sublists.sort(key=len, reverse=False)
    _calc_subsets = map(set, _calc_sublists)

    applied_sets = util.AppliedSets()        

    for i in range(len(_calc_subsets)):                                         
        if applied_sets.check(_calc_subsets[i]) == False:  
            _calc_left_parts = []
            selected_calc_ids = _calc_subsets[i]
            for s in selected_calc_ids:
                _calc_left_parts.extend(util.get_calc_relation_by_id(_calc_relations, s).left_part) 
            #we need to use calc_relations whose left parts don't intersect and all together are equal to student_rightmost_notations
            if (len(filter(lambda x: x in student_rightmost_notations, set(_calc_left_parts))) == len(student_rightmost_notations)):   
                _calc_right_parts, _calc_ids = [], []
                for s in selected_calc_ids: 
                    _calc_right_parts.append(util.get_calc_relation_by_id(_calc_relations, s).right_part)
                    _calc_ids.append(s)
                solution_paths.append(calc.Path(_calc_right_parts, student_rightmost_notations, _calc_ids))
                applied_sets.update(selected_calc_ids) 
                
    return solution_paths

def get_relations_intersecting_with_student_rightmost_notations(_calc_relations, student_rightmost_notations):

    selected_calc_relations = []
    for j in range(len(_calc_relations)):
        if (len(filter(lambda x: x in student_rightmost_notations, _calc_relations[j].left_part)) > 0):
            selected_calc_relations.append(_calc_relations[j].get_id())
    return selected_calc_relations
   
  
def get_dependencies_from_paths(_calc_relations, solution_paths):

    dependencies = []
    for i in range(len(solution_paths)):
        path = solution_paths[i]
        if path.found == True:
            formulas_list = []
            for j in range(len(path.indexes)):
                formulas_list.append(_calc_relations[path.indexes[j]].get_id())
            dependencies.append(formulas_list)
    return dependencies

def get_filtered_solution_paths(solution_paths):
    return filter(lambda x: x.found == False, solution_paths)
   
def get_new_paths_by_expanding_existing_paths(_calc_relations, solution_paths, student_leftmost_notations):
    #попытаемся продвинуть вперед каждый возможный путь                                   
    new_solution_paths = []
    for i in range(len(solution_paths)):
        path = solution_paths[i]
        new_solution_paths.extend(get_possible_solution_paths(_calc_relations, student_leftmost_notations, path))
    return new_solution_paths

def get_updated_solution_paths(new_solution_paths):
    solution_paths = []
    if (len(new_solution_paths) > 0):
        solution_paths = copy.deepcopy(new_solution_paths)
    return solution_paths

def show_answer(calc_relations, dependencies, student_formula): 
    s = []
    if (len(dependencies) > 0):
        for i in range(len(dependencies)):
            formulas_text = map(lambda x: get_formula_text(calc_relations, x), dependencies[i])
            s.append(u'формула студента ' + student_formula + ' получена комбинацией формул:' + ', '.join(formulas_text))
    else:
        s.append('не удалось распознать формулу, введенную студентом')
    return s

def get_formula_text(_calc_relations, selected_id):
    cr = util.get_calc_relation_by_id(_calc_relations, selected_id)
    return cr.formula_text    
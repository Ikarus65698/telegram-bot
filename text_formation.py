import numpy as np
import re
import exchange_list as ex

def convert_to_range(x):

    if (type(x) == int):

        numbers = []

        for i in range(0, x + 1):
            numbers.append(int((-1) * (x - i)))

        for i in range(1, x + 1):
            numbers.append(int(i))

        return numbers

    elif (type(x) == str):

        if (x.find(' ') == -1) or (x.find(',') == -1):

            x = int(x)
            numbers = []

            for i in range(0, x + 1):
                numbers.append(int((-1) * (x - i)))

            for i in range(1, x + 1):
                numbers.append(int(i))

            return numbers
        
        else:
            return [int(i) for i in re.findall(r'-?\d+', x)]
    
    elif (type(x) == list):
        return x

    else:
        return TypeError

def take_parametr(string):
    
    x_str = []
    y_str = []
    flag = True

    for i in string:

        if (i == '='):
            flag = False
            continue

        if (flag) and (i != ' '):
            x_str.append(i)
            continue

        if (not flag) and (i != ' '):
            y_str.append(i)

    new_x_str = ''.join(x_str).lower()
    new_y_str = ''.join(y_str).lower()

    return [new_x_str, new_y_str]

def transform_to_func(list_of_parm, func):

    end_list = []

    if (type(list_of_parm) == int) or (type(list_of_parm) == str):
        list_of_parm = convert_to_range(list_of_parm)

    for i in list(ex.change.keys()):
        if (func.find(i) != -1):
            func = func.replace(i, ex.change.get(i))

    if (func.find('x') != -1):
        trans_func = lambda x: eval(func)

    if (func.find('y') != -1):
        trans_func = lambda y: eval(func)

    for i in list_of_parm:
        end_list.append(trans_func(i))

    return end_list

def translit(string):

    language = True # True - eng; False - rus
    up_case = []

    for i in range(len(string)):
        if (string[i].isupper()):
            up_case.append(i)

    string = list(string.lower())

    for letter in string:
        if (letter in ex.egn_to_rus.values()):
            language = False
            break

    if (language):
        for i in range(len(string)):

            if (string[i] in ''.join(ex.egn_to_rus.keys())):
                string[i] = ex.egn_to_rus.get(string[i])

        

    else:
        for i in range(len(string)):

            if (string[i] in ''.join(ex.rus_to_eng.keys())):
                string[i] = ex.rus_to_eng.get(string[i])


    for i in up_case:
        string[i] = string[i].upper()

    return ''.join(string)

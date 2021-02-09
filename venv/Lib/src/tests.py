
from Lib.src.cfg import *
import Lib.src.statements_template as st
import xlsxwriter

import matplotlib.pyplot as plt


data = statements_templates.BALANCE_SHEET_TEMPLATE

def add_data_to_statement(key : str,
             d : dict,
             data_to_write : dict):
    if (key in d.keys()):
        temp   = d[key]
        temp.update(data_to_write)
        d[key] = temp
        return d
    else:
        for kid in d.keys():
            d[kid] = find_key(key, d[kid], data_to_write)
            return d

def get_score(inp, options):
    breakdown = inp.split()
    
    score = 0
    
    for word in breakdown:
        for o in options:
            score += _utils.levenshtein(inp, o)    
    return score

import pickle


# with open('/home/avshalom/Documents/python_projects/stock_analysis/stocks/venv/DB/GME/GME.pkl', 'rb') as f:
#     data = pickle.load(f)

# print(data["balance"])


import re
text = "income tax (expense) benefit"
pat = "\(.*\)"
r = re.search(pat, text)
if (r):
    print(r.group(0).replace("(","").replace(")",""))



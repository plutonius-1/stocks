import numpy as np
import os, sys
import pandas as pd
import difflib

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    # print (matrix)
    return (matrix[size_x - 1, size_y - 1])

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
            if (type(d[kid]) == dict):
                d[kid] = add_data_to_statement(key, d[kid], data_to_write)
                # return d
        return d
    

    
    
def is_date_in_tag(tag : str,
                   date : str,
                   dic):
    """
    looks for the the 'date' in 'tag' return True or None
    """
    if (tag in dic.keys()):
        if (date in dic[tag]):
            return True
        
    else:
        for k in dic.keys():
            if (type(dic[k]) == dict):
                if (is_date_in_tag(tag, date, dic[k])) == True:
                    return True
        
        
        
def force_best_match_in_df(df           : pd.DataFrame,
                           name_to_find : str):
    # print(list(df.index))
    
    best_match = ""
    base_cutoff = 0.6
    best_matches = []
    OPTIONS_WANTED = 3
    
    # best_matches = difflib.get_close_matches(name_to_find, list(df.index))
    # if (len_best_matches == 0):
    new_df = df
    new_df.index = df[df.columns[0]]
    candidats = [str(i) for i in new_df.index if not pd.isna(i)]
        
    while base_cutoff > 0:
        # print("name to find :", name_to_find)
        # print("index: ", list(df.index))
        best_matches = difflib.get_close_matches(name_to_find, candidats,n=len(new_df.index), cutoff = base_cutoff)
        base_cutoff -= 0.02

    # print("best matches so far: ", best_matches)
    sorted_list = []
    partial_words_tags = []
    for tag in best_matches:
        sub_words_match = 0
        for sub_word in name_to_find.split():
            if (sub_word in tag.lower()):
                sub_words_match += 1
        if (sub_words_match == len(name_to_find.split())):
            sorted_list.append(tag)
        elif (sub_words_match < len(name_to_find.split()) and sub_words_match > 0):
            partial_words_tags.append(tag)

    best_matches = []
    base_cutoff = 0.6
    while len(best_matches) == 0 and base_cutoff > 0:
        best_matches = difflib.get_close_matches(name_to_find, sorted_list, cutoff = base_cutoff)
        base_cutoff -= 0.02
        
    if (len(best_matches) > 0):
        print("best match found: ", best_matches[0])
        print("values = ", new_df.loc[best_matches[0]].values)
        return new_df.loc[best_matches[0]].values[1]
    else:
        return None

def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))


def find_DB_dir():

    curr_dir_name = os.getcwd().split("\\")[-1]
    full_path     = __file__
    new_path      = os.getcwd()
    platfrom      = sys.platform
    
    if (platfrom == "linux"):
        return "/home/avshalom/Documents/python_projects/stock_analysis/stocks/venv/DB/"
    if (platfrom == "window"):
        return None ## TODO
    # while curr_dir_name != "venv":
    #     print(new_path)
    #     # windows
    #     if (sys.platform == "windwos"):
    #         new_path = [i + "/" for i in new_path.split("\\")[:-2]]
            
    #     if (sys.platform == "linux"):
    #         new_path = [i + "/" for i in new_path.split("/")[:-2]]
    #     new_path = "".join(new_path)
        
    #     curr_dir_name = new_path[-1].replace("/","").replace("\\","")


    # return "".join(new_path) + "/DB/"
    

test_dic = {'income': {'Net income attributable to 3M': 1, 'b': 2,
                       "Net income including noncontrolling interest":1,
                       "Weighted average 3M common shares outstanding - diluted (in shares)":2,
                       "operating income":2}}
# print(is_date_in_tag("g","sub",test_dic))
# df = pd.DataFrame(data = test_dic)
# force_best_match_in_df(df, "net income")
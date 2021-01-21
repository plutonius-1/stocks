
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


counts = {}
pbs    = {}
for i in range(1,70):
    if (i >= 1 and i < 10):
        key = "0"+str(i)
    else:
        key = str(i)

    counts[key] = 0

for i in range(1,40):
    if (i >= 1 and i < 10):
        key = "0"+str(i)
    else:
        key = str(i)
    pbs[key] = 0


df = pd.read_csv("C:/Users/avsha/Downloads/Lottery_Powerball_Winning_Numbers__Beginning_2010(1).csv")
numbers = df["Winning Numbers"]


max_ps = 0
for row in numbers:
    t =     int(row.split()[-1])
    if (int(row.split()[-1]) > max_ps):
        max_ps = t

for row in numbers:
    split = row.split()
    for i in range(len(split) - 1):
        counts[split[i]] += 1

    pbs[split[i + 1]] += 1

nums = list(counts.keys())
hits = list(counts.values())


# fig = plt.figure()
# ax = fig.add_axes([100,100])
# ax.bar(nums, hits
# plt.bar(nums, hits)
# plt.show()
# plt.hist(hits)
# plt.show()
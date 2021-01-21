# from Lib.src.cfg import *
import numpy as np
from bs4 import BeautifulSoup
html_doc = "C:/Users/avsha/Downloads/file_types/0001564590-20-050472.txt"

with open(html_doc) as fp:
    soup = BeautifulSoup(fp, 'html.parser')

print(soup.head)





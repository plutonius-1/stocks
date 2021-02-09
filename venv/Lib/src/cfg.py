from __future__ import print_function
import numpy as np
import requests as reqs
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import csv
import sys
from dateutil.parser import parse
import Lib.src.comp_tree_c as comp_tree_c
import difflib
import pickle
import Lib.src.statements_template as statements_templates
import Lib.src.utils as _utils

#####################
#      CONSTS       #
#####################

SEC_ARCHIVE_COMPANIES_INDEX = 'https://www.sec.gov/Archives/edgar/full-index/'
SEC_ARCHIVE_BASE            = "https://www.sec.gov/Archives/"
TEMP_YEAR                   = "temp_year.html"
TEMP_COMPANIES_INDEX_NAME   = "temp_companies_index.txt"
TEMP_COMPANIES_QTR_INDEX_NAME = "temp_companies_index"
TEMP_IDX_FILE_TYPE          = ".txt"
TEMP_XLSX_FILE_NAME         = "tmp_xlsx_file.xlsx"
#COMPANIES_DB_BASE_PATH      = "C:/Users/avsha/Documents/python_envs/stock_analysis_env/venv/DB/"
COMPANIES_DB_BASE_PATH      = _utils.find_DB_dir()
DB_FILE_FORMAT              = ".pkl"

### CIK CONSTS ###
CIK_URL = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'
CIK_RE = re.compile(r'.*CIK=(\d{10}).*')
##################

FINANCIAL_REPORT_POSTFIX = "Financial_Report.xlsx"
WRITE       = "w"
READ        = "r"
URL_POSTFIX = "/"
HTML_LINK_TYPE = "a"
HTML_HREF_TYPE = "href"
HTML_PARSER    = "html.parser"
### functions ###
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
#################


################ MISC #####################
THOUSNADS = 1000
MILLIONS  = 1000000
BILLIONS  = 1000000000
TITLE_ROW = "title_row"
TOTAL_ROW = "total_row"


########### COMP DATA HANDLER ###########
INCOME_WANTED_NAMES_LIST   = ["income", "revenue", "operations"]
INCOME_UNWANTED_NAMES_LIST = ["comprehensive", "parent"]
INCOME_MUST_HAVE_NAMES_LIST = []
BALANCE_WANTED_NAMES_LIST   = ["balance", "sheet"]
BALANCE_UNWANTED_NAMES_LIST = ["comprehansive", "parent"]
BALANCE_MUST_HAVE_NAMES_LIST = []
CASH_FLOW_MUST_HAVE_NAMES = ["cash", "flow"]

#########################################
INCOME   = "income"
BALANCE  = "balance"
CASHFLOW = "cashflow"

CURRENT_ASSETS_S = "current assets"
NON_CURRENT_ASSETS_S = "non-current assets"
CURRENT_LIABILITIES_S = "current liabilities"
NON_CURRENT_LIABILITIES_S = "non-current liabilities"

BALANCE_SHEET_TYPES = [CURRENT_ASSETS_S, NON_CURRENT_ASSETS_S, CURRENT_LIABILITIES_S, NON_CURRENT_LIABILITIES_S]
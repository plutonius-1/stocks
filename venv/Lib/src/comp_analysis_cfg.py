from Lib.src.cfg import *

##### Constst ####

## ASSETS ##
FINANCIAL_ASSETS_LABELS = ["cash and cash equivalents",
                           "marketable securities",
                           "cash"] # TODO
FINANCIAL_ASSETS_PATT = ""
############


## LIABILITIES ##
FINANCIAL_LIABILITISE_LABELS = []
FINANCIAL_LIABILITISE_PATT = ""
#################



##################


def format_tags(tag : str,
                type : str):
    if (type != INCOME and type != BALANCE and type != CASHFLOW):
        print("in format_tags: - type is invalid", type)
        return

    if (type == BALANCE):
        pass

def is_line_a_title(val):
    if (pd.isna(val)):
        return True
    return False

BALANCE_SHEET_TITLES = [
                        "current_assets",
                        "inventories",
                        "inventory",
                        "current liabilities",
                        "non-current assets",
                        "stockholders’ equity",
                        "shareholders’ equity"
                        ]

def format_statement_line(line,
                          type: str):
    if (type != INCOME and type != BALANCE and type != CASHFLOW):
        print("in format_tags: - type is invalid", type)
        return

    tag, val = line[0], line[1]

    if (type == BALANCE):
        if (is_line_a_title(val)):
            for title in BALANCE_SHEET_TITLES:
                if (title in tag):






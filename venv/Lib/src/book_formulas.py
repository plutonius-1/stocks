import pandas as pd

OPERATIONAL_ASSETS_NET = "operational_assetst_net"
FINANCIAL_ASSETST_NET  = "financial_assets_net"
SURPLUS_ASSETST_NET    = "surplus_assetst_net"

BOOK_TYPES = [OPERATIONAL_ASSETS_NET, FINANCIAL_ASSETST_NET, SURPLUS_ASSETST_NET]
PRECENT_OF_CASH_USED_IN_OPERATIONS = 0.02
########################
###### Assets ##########
########################


operational_assets_tags = [
    "inventories",
    "cash",
    "other current assets",
    "goodwill",
    "receivables",
    "prepaid",
    "pre-paid",
    "total current assets"
    "property",
    "plant",
    "equipment",
    "intangibles",
    "intangible",
    "deffered tax",
    "deffered",
]

finanicial_assetst_tags = [
    "cash",
    "marketable securities",
    "marketable",
    "lease",
]

surplus_assets_tags     = [
    "pension",
    "postretirement",
    "post retirement",
]

long_term_assets_tags   = [
]


###############################
######### Liabilities #########
###############################

operational_liablities_tags = [
    "pension",
    "postretirement",
    "post retirement",
    "deffered tax",
    "deffered",
    "other",
    "intangibles",
    "intangible"
    "lease",
    "payable",
    "accrued expenses",
    "expenses"
]

finanicial_liabilities_tags = [
    "borrowings",
    "borrow",
    "long term debt",
    "short term debt",
    "debt"

]

def prase_net_financial_assets(assets_df  : pd.DataFrame,
                               liab_df    : pd.DataFrame,
                               ):
    assets_data      = {}
    liabilitied_data = {}
    net_data         = {}
    # asssets side
    for row_idx in range(len(assets_df.index)):

        tag,val = assets_df.iloc[row_idx,0].lower(), assets_df.iloc[row_idx,1]

        for name in finanicial_assetst_tags:
            if ((name in tag or tag in name) and (not pd.isna(val))):
                assets_data.update({tag:val})
    assets_data.update({"total":sum(list(assets_data.values()))})

    # liabilities side
    for row_idx in range(len(liab_df.index)):

        tag, val = liab_df.iloc[row_idx, 0].lower(), liab_df.iloc[row_idx, 1]

        for name in finanicial_liabilities_tags:
            if ((name in tag or tag in name) and (not pd.isna(val))):
                liabilitied_data.update({tag: val})
    liabilitied_data.update({"total":sum(list(liabilitied_data.values()))})
    net = (assets_data["total"] - liabilitied_data["total"])
    net_data.update({"net":net})
    return net_data

def get_net_assets(assets_df         : pd.DataFrame,
                   postive_keywords  : list,
                   liab_df           : pd.DataFrame,
                   negative_keywords : list,
                   type
                   ):

    assets_data      = {}
    liabilitied_data = {}
    net_data         = {}
    # asssets side
    for row_idx in range(len(assets_df.index)):

        tag,val = assets_df.iloc[row_idx,0].lower(), assets_df.iloc[row_idx,1]

        for name in postive_keywords:
            if ((name in tag or tag in name) and (not pd.isna(val))):
                assets_data.update({tag:val})

    if (type not in BOOK_TYPES):
        print("type: {} is not one of : {}".format(type, ", ".join(BOOK_TYPES)))
        return
    else:
        if (type == OPERATIONAL_ASSETS_NET):
            for tag in list(assets_data.keys()):
                if "cash" in tag:
                    assets_data[tag] = PRECENT_OF_CASH_USED_IN_OPERATIONS * assets_data[tag]
    assets_data.update({"total":sum(list(assets_data.values()))})

    # liabilities side
    for row_idx in range(len(liab_df.index)):

        tag, val = liab_df.iloc[row_idx, 0].lower(), liab_df.iloc[row_idx, 1]

        for name in negative_keywords:
            if ((name in tag or tag in name) and (not pd.isna(val))):
                liabilitied_data.update({tag: val})
    liabilitied_data.update({"total":sum(list(liabilitied_data.values()))})
    net = (assets_data["total"] - liabilitied_data["total"])
    net_data.update({"net":net})
    return assets_data, liabilitied_data, net_data

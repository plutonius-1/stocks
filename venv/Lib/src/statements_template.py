import difflib

BALANCE_SHEET_TEMPLATE = {

    "assets":{
        "current":{
            "cash & short term investments":{
                "cash only":{},
                "short-term investments":{},
                "total":{}
            },

            "accounts receivable detailed":{
                "accounts receivables":{},
                "bad debt/doubtful accounts":{},
                "other receivables":{},
                "total":{}
            },

            "prepaids":{"total":{}},

            "inventories":{"total":{}},

            "other current assets":{"total":{}},

            "total current assets":{"total":{}},
        },

        "non current":{

            "net property, plant & equipment":{
                "property, plant & equipment":{},
                "accumulated depreciation":{},
                "total(net)":{}
            },

            "total investments and advances":{
                "other long-term investments":{"total":{}}
            },

            "long-term note receivables":{"total":{}},

            "intangible assets":{
                "net goodwill":{},
                "net other intangibles":{},
                "total":{}
            },

            "lease assets":{"total":{}},

            "other lt assets":{"total":{}},

            "total assets":{"total":{}}
        }


    },


    "liabilities":{

        "current" : {

            "short term debt":{"total":{}},

            "accounts payable":{"total":{}},

            "accrued expenses":{"total":{}},

            "other current liabilities":{"total":{}},

            "total current liabilities":{"total":{}},
        },

        "non current" : {

            "long term debt":{"total":{}},

            "lease obligations":{"total":{}},

            "provisions":{"total":{}},

            "pension":{"total":{}},

            "deferred taxes":{"total":{}},

            "other lt liabilities":{"total":{}},

            "deferred income":{"total":{}},

            "total liabilities":{"total":{}}
        }
    },


    "equity":{

        "preferred stock":{"total":{}},

        "common equity":{

            "common stock":{},

            "retained earnings":{},

            "debt guarantee":{},

            "cumulative translation adjustment/unrealized for. exch. gain":{},

            "unrealized gain/loss marketable securities":{},

            "revaluation reserves":{},

            "treasury stock":{},

            "total":{}
        },

        "total shareholders' equity":{"total":{}},

        "accumulated minority interest":{"total":{}},

        "total equity":{"total":{}},

        "liabilities & shareholders' equity":{"total":{}}
    }

}

CASH_FLOW_TEMPLATE = {}

INCOME_STATEMENT_TEMPLATE = {}


######################################
## BALANCE SHEET TYPES ##

ASSETS_ST = "short term assets"
ASSETS_LT = "long term assets"
LIABILATIES_ST = "short term liabilities"
LIABILATIES_LT = "long term liabilities"

###################################
#### ASSETST CANDIDATES LISTS #####
cash_only_cands = {"cash only":["cash and cash equivalents", "cash"]}
short_term_investments_cands = {"short-term investments":["short term investments", "marketable securities", "securities", "marketable"]}
accounts_receivable_cands    = {"accounts receivables":["accounts receivables", "receivables", "trade receivables"]}
other_receivables_cands = {"other receivables":["other receivables", "receivables other"]}
inventories_cands = {"inventories":["inventories", "total inventories", "inventories total", "inventory"]}
prepaids_cands             = {"prepaids":["prepaid", "prepaids"]}
other_current_assets_cands = {"other current assets":["other current assets", "other assets", "assets other"]}
total_current_assets_cands = {"total current assets":["total current assets", "total assets current"]}
property_plant_equipment_cands = {"property, plant & equipment":["property, plant & equipment","property plant equipment"]}
accumulated_depreciation_cands = {"accumulated depreciation":["accumulated depreciation","depreciation"]}
other_long_term_investments_cands = {"other long-term investments":["other long-term investments","long term investments"]}
long_term_note_receivables_cands  = {"long-term note receivables":["long-term note receivables","long term receivables"]}
net_goodwill_cands                = {"net goodwill":["net goodwill","goodwill"]}
other_intangibles_cands           = {"net other intangibles":["net other intangibles","other intangibles","intangibles"]}
lease_assets_cands                = {"lease assets":["lease","lease assets"]}
other_lt_assets_cands             = {"other lt assets":["other long term assets"]}
total_assets_cands                = {"total assets":["total assets"]}

#######################################
#### LIABILITIES CANDIDATES LISTS #####

short_term_debt_cands = {"short term debt":["short term debt","short term borrowing", "current debt"]}
long_term_debt_cands  = {"long term debt":["long term debt"]}
accounts_payable_cands = {"accounts payable":["accounts payable"]}
accrued_expenses_cands          = {"accrued expenses":["accrued expenses"]}
other_current_liablities_cands  = {"other current liabilities":["other current liabilities", "other"]}
total_current_liabilities_cands = {"total current liabilities":["total current liabilities"]}
lease_obligations_cands         = {"lease obligations":["lease obligations","lease","operating lease"]}
provisions_cands                = {"provisions":["provisions"]}
pension_cands                   = {"pension":["pension", "postretirement"]}
deferred_taxes_cands            = {"deferred taxes":["deferred taxes"]}
other_lt_liabilities_cands      = {"other lt liabilities":["other lt liabilities", "other long term liabilities"]}
deferred_income_cands           = {"deferred income":["deferred income"]}
total_liabilities_cands         = {"total liabilities":["total liabilities"]}

def convert_naming_convention(input : str,
                              type  : str):

    max_group_name = ""
    max_group      = 0
    cands_groups   = []

    if (type == ASSETS_ST):
        cands_groups = [cash_only_cands,
                        short_term_investments_cands,
                        accounts_receivable_cands,
                        other_receivables_cands,
                        inventories_cands,
                        prepaids_cands,
                        other_current_assets_cands,
                        total_current_assets_cands]

    elif (type == ASSETS_LT):
        cands_groups = [property_plant_equipment_cands,
                        accumulated_depreciation_cands,
                        other_long_term_investments_cands,
                        long_term_note_receivables_cands,
                        net_goodwill_cands,
                        other_intangibles_cands,
                        lease_assets_cands,
                        other_lt_assets_cands,
                        total_assets_cands]

    elif (type == LIABILATIES_ST):
        cands_groups = [short_term_debt_cands,
                        accounts_payable_cands,
                        accrued_expenses_cands,
                        other_current_liablities_cands,
                        total_current_liabilities_cands]

    elif (type == LIABILATIES_LT):
        cands_groups = [long_term_debt_cands,
                        lease_obligations_cands,
                        provisions_cands,
                        pension_cands,
                        deferred_taxes_cands,
                        deferred_income_cands,
                        other_lt_liabilities_cands,
                        total_liabilities_cands]


    for group in cands_groups:
        g_max = 0
        candidates = difflib.get_close_matches(input, list(group.values())[0])

        for g in candidates:
            res = difflib.SequenceMatcher(None, input, g).ratio()
            if (res > g_max):
                g_max = res
        if (g_max > max_group):
            max_group = g_max
            max_group_name = list(group.keys())[0]
    print("input: ", input, "max name: ", max_group_name)

    return max_group_name






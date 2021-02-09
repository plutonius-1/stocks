import difflib
import re

def expense_or_income(text_to_check : str):
    expense_key_words = ["expense", "loss", "expenses", "losses"]
    income_key_words  = ["income", "benefit", "benefits", "incomes"]
    pat = "\(.*\)"
    search = re.search(pat, text_to_check)
    if (search):
        t = search.group(0).replace("(","").replace(")","")
        if (t in expense_key_words):
            return -1
        elif (t in income_key_words):
            return 1
        else:
            return None
    return None



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

INCOME_STATEMENT_TEMPLATE = {
    
    "revenue":{"total":{}},
    
    "cost of sales":{"total":{}},
    
    "depreciation & amortization expense":{"total":{}},
    
    "gross income":{"total":{}},
    
    "sg&a expense":{"total":{}},

    "r&d expense":{"total":{}},

    "unusual expense":{"total":{}},

    "unusual income":{"total":{}},

    "ebit":{"total":{}},
    
    "non operating income":{"total":{}},

    "non operating expense":{"total":{}},
    
    "non-operating interest income":{"total":{}},
    
    "interest revenue":{"total":{}},
    
    "interest expense":{"total":{}},
    
    "pretax income":{"total":{}},
    
    "income tax":{"total":{}},
    
    "net income":{"total":{}},
    
    "net loss":{"total":{}},
    
    "dividends":{"total":{}},
    
    "eps":{"total":{}},
    
    "eps (diluted)":{"total":{}},
    
    "ebitdat":{"total":{}} # TODO
    }


######################################
## BALANCE SHEET TYPES ##
EQUITY   = "equity"
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
lease_assets_cands                = {"lease assets":["lease","lease assets","operating lease","lease assets"]}
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
lease_obligations_cands         = {"lease obligations":["lease obligations","lease","operating lease","lease liabilities"]}
provisions_cands                = {"provisions":["provisions"]}
pension_cands                   = {"pension":["pension", "postretirement"]}
deferred_taxes_cands            = {"deferred taxes":["deferred taxes"]}
other_lt_liabilities_cands      = {"other lt liabilities":["other lt liabilities", "other long term liabilities"]}
deferred_income_cands           = {"deferred income":["deferred income"]}
total_liabilities_cands         = {"total liabilities":["total liabilities"]}

######################################
###### EQUITY CANDIDATES LIST ########
preferred_stock_cands = {"preferred stock":["preferred stock"]}
common_stock_cands    = {"common stock":["common stock"]}
retained_earnings_cands = {"retained earnings":["retained earnings"]}
debt_guarantee_cands    = {"debt guarantee":["debt guarantee"]}
cumulative_translation_adjustment_exch_cands = {"cumulative translation adjustment":["cumulative translation adjustment exch"]}
unrealized_gain_loss_marketable_securities_cands = {"unrealized gain/loss marketable securities":["unrealized gain/loss marketable securities","unrealized gain loss","gain loss marketable securities"]}
revaluation_reserves_cands = {"revaluation reserves":["revaluation reserves"]}
treasury_stock_cands = {"treasury stock":["treasury stock"]}
total_shareholders_equity_cands = {"total shareholders' equity":["total shareholders' equity"]}
accumulated_minority_interest_cands = {"accumulated minority interest":["accumulated minority interest","minority interest","Noncontrolling interest","Non controlling interest"]}
total_equity_cands   = {"total equity":["total equity"]}
liabilities_shareholders_equity_cands = {"liabilities & shareholders' equity":["liabilities & shareholders' equity"]}

#####################################
###### INCOME STATEMENT #############

#####################################
######### TYPES######################
INCOME = "income"
INCOME_PER_SHARE = "income per share"

############################################
############ INCOME CANDIDATES LIST ########
revenue_cands = {"revenue":["revenue", "revenues", "net revenue","net revenues", "net sales", "sales"]}
cost_of_goods_cands = {"cost of sales":["total cost of sales", "cost of sales", "cost of sales", "total operating expenses", "operating expenses"]}
depreciation_amortization_expense_cands = {"depreciation & amortization expense":["depreciation & amortization expense","depreciation amortization", "total depreciation amortization", "depreciation and amortization"]}
gross_income_cands = {"gross income":["operating income", "total gross income", "gross incomei","operating income"]}
sga_expense_cands = {"sg&a expense":["selling, administrative, and other expenses","general and administrative expenses", "selling, general and administrative expenses"]}
rd_expense_cands  = {"r&d expense":["research, development and related expenses", "technology and development", "research and development", "research & development"]}
unusual_expense_cands = {"unusual expense":["unusual expense"]}
unusual_income_cands =  {"unusual income": ["unusual income"]}
ebit_cands           = {}
non_operating_income_cands  = {"non operating income":["other income (expense), net", "other income (expense)", "other income"]}
non_operating_expense_cands = {"non operating expense":["other expense (income)", "other expense"]}
interest_expense_cands      = {"interest expense":["interest expense"]}
interest_revenue_cands      = {"interest revenue":["interest revenue"]}
pretax_income_cands         = {"pretax income":["income before taxes","pretax income","loss before taxes", "before taxes", "income (loss) before income tax","loss (income) before income tax"]}
income_tax_cands            = {"income tax":["income tax","income taxes"]}
net_income_cands            = {"net income":["net income"]}
net_loss_cands              = {"net loss":["net loss"]}
dividends_cands             = {"dividends":["dividends"]}

###############################################
################ PER SHARE CANDIDATES #########
eps_cands                   = {"eps":["earnings per share","basic earning","income per share","basic per share", "basic"]}
eps_diluted_cands           = {"eps (diluted)":["earnings per share (diluted)","diluted earning","income per share diluted","diluted per share", "diluted"]}



def convert_naming_convention(input : str,
                              type  : str):
    """
    input: - str: the name to convert to template 
    type:  - what kind of statement? balance long/short? income? CF?
    """

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
        
    elif (type == EQUITY):
        cands_groups = [
            preferred_stock_cands,
            common_stock_cands,
            retained_earnings_cands,
            debt_guarantee_cands,
            cumulative_translation_adjustment_exch_cands,
            unrealized_gain_loss_marketable_securities_cands,
            revaluation_reserves_cands,
            treasury_stock_cands,
            total_shareholders_equity_cands,
            accumulated_minority_interest_cands,
            total_equity_cands,
            liabilities_shareholders_equity_cands]


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

    return max_group_name






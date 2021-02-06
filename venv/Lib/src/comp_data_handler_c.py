from Lib.src.cfg import *
import Lib.src.utils as _utils
from Lib.src.book_formulas import *

current_assets_template = {
    "cash and cash equivalents":{},
    "marketable securities":{},
    "receivable":{},
    "inventories":{},
    "prepaids":{},
    "other current assets":{},
    "total current assets":{}
}

non_current_assetes_template = {
    "property plant and equipment":{},
    "depreciation":{},
    "marketable securities":{},
    "property plant and equipment - net":{},
    "goodwill":{},
    "intangible assets":{},
    "other non current assets":{},
    "total non current assets":{}
}

total_assetes_template = {
    "total current assets":{},
    "total non current assets":{},
    "total assets":{}
}


current_liabilities_template = {
    "short term borrowings":{},
    "accounts payable":{},
    "accrued payroll":{},
    "accrued income taxes":{},
    "other current liabilities":{},
    "total current liabilities":{}

}

non_current_liabilities_template = {
    "long term":{},
    "pensions":{},
    "other non current liabilities":{},
    "total non current liabilities":{}
}

total_liabilities_template = {
    "total current liabilities":{},
    "total non current liabilities":{},
    "total liabilities": {}
}

balance_sheet_template = {
    "current_assets":{"total_current_assets":None},
    "non_current_assets":{"total_non_current_assets":None},
    "other_assets":{"total_other_assets":None},
    "total_assets":{"total_assets":None},
    "current_liabilaties":{"total_current_liabilaties":None},
    "non_current_liabilities":{"total_non_current_liabilaties":None},
    "other_liabiities":{"total_other_liabilities":None},
    "total_liabilities":{"total_liabilities":None}
}

class comp_data_handler_c:

    def __init__(self, ticker = None):
        self.ticker      = ticker
        self.db_path     = None
        self.comp_data   = None

        self.temp_date   = None
        
        ## Statements ##
        self.b_s         = None # balance sheet
        self.inc_s       = None # income statement
        self.cash_s      = None # cash flow statement

        self.temp_b_s    = pd.DataFrame
        self.temp_b_s_flag = False
        self.temp_inc_s  = None
        self.temp_inc_s_flag = False
        self.temp_cash_s = None
        self.temp_cash_s_flag = False

        ## Init Functions ##
        self.temp_date = self.get_doc_date()

    def get_comp_db(self, ticker : str):
        """
        looks for a companys DB - if not exists - create a dir and a template for balance, income and cash
        flow dics
        :param ticker:
        :return:
        """
        if (not os.path.isdir(COMPANIES_DB_BASE_PATH)):
            os.makedirs(COMPANIES_DB_BASE_PATH)
        
        # set the ticker for the entire handler

        self.ticker = ticker
        if (os.path.isdir(COMPANIES_DB_BASE_PATH + self.ticker)):
            self.db_path = COMPANIES_DB_BASE_PATH + self.ticker + "/" + (self.ticker + DB_FILE_FORMAT)
            f = open(self.db_path, "rb")
            self.comp_data = pickle.load(f)

        else:
            # create the folder
            os.makedirs(COMPANIES_DB_BASE_PATH + self.ticker)

            # download all company data using request handler
            # self.request_handler.get_year_data()
            
            # 
            self.crate_db_template()
    
    
    def update_local_pkl(self, dic_to_update):
        pkl_path  = COMPANIES_DB_BASE_PATH + self.ticker + "/"
        f = open(pkl_path + self.ticker + DB_FILE_FORMAT, "wb")
        pickle.dump(dic_to_update, f)
        f.close()

        return

    def crate_db_template(self):
        """
        crate an empty balance, income, cashflow statements and saves the union of all of them
        :return:
        """
        # create the folder
        #os.makedirs(COMPANIES_DB_BASE_PATH + self.ticker)

        # crate empty templates
        pkl_path  = COMPANIES_DB_BASE_PATH + self.ticker + "/"

        # sheets
        balance_template   = statements_templates.BALANCE_SHEET_TEMPLATE
        income_template    = statements_templates.INCOME_STATEMENT_TEMPLATE
        cash_flow_template = statements_templates.CASH_FLOW_TEMPLATE

        comp = {INCOME:income_template,
                BALANCE:balance_template,
                CASHFLOW:cash_flow_template}

        self.comp_data = comp
        f = open(pkl_path + self.ticker + DB_FILE_FORMAT, "wb")
        pickle.dump(comp, f)
        f.close()
        return

    def parse_sheets_names(self,
                           input,
                           must_have : list,
                           wanted    : list,
                           unwanted  : list):
        """
        Goes over the titles of sheet from excel file - and makes sure they fit the income, balance and cashflow
        statements
        :param input: sheets name
        :param must_have: strings that must be in sheet name
        :param wanted: strings that wanted to be in sheet name
        :param unwanted: strings that must not be in sheet name
        :return: logic valeu
        """
        for i in unwanted:
            if (i in input.lower()):
                return False

        for i in must_have:
            if (i not in input.lower()):
                return False

        for i in wanted:
            if (i in input.lower()):
                return True
        return False

    def get_temp_sheets(self):
        """
        assigns income, balance, cashflow statements to temp variables from a temporary CSV file from SEC.
        :return:
        """
        def check_all_docs_found():
            if (self.temp_b_s_flag == True and self.temp_inc_s_flag == True and self.temp_cash_s_flag == True):
                return True
            return False

        indexes = []
        d = pd.read_excel(TEMP_XLSX_FILE_NAME, None,
                         engine="openpyxl")

        for i in range(len(d.keys())):
            d = pd.read_excel(TEMP_XLSX_FILE_NAME,
                              i,
                              index_col = None,
                              header = None,
                              # usecols='A:E',
                              # nrows = 0,
                              engine='openpyxl')
            col_name = d.iat[0,0]
            if (col_name != None):
                col_name = col_name.lower()
                if self.parse_sheets_names(col_name, INCOME_MUST_HAVE_NAMES_LIST, INCOME_WANTED_NAMES_LIST, INCOME_UNWANTED_NAMES_LIST):
                    self.temp_inc_s = d
                    self.temp_inc_s_flag = True
                    if check_all_docs_found(): break
                if (self.parse_sheets_names(col_name, CASH_FLOW_MUST_HAVE_NAMES, ["statement", "cash", "flow"], ["comprehansive", "parent"])):
                    self.temp_cash_s = d
                    self.temp_cash_s_flag = True
                    if check_all_docs_found(): break
                if (self.parse_sheets_names(col_name, BALANCE_MUST_HAVE_NAMES_LIST, BALANCE_WANTED_NAMES_LIST, BALANCE_UNWANTED_NAMES_LIST)):
                    self.temp_b_s = d
                    self.temp_b_s_flag = True
                    if check_all_docs_found(): break
        return

    def get_doc_date(self):
        d = pd.read_excel(TEMP_XLSX_FILE_NAME,
                          0,
                          index_col = 0,
                          engine="openpyxl")

        dt = None
        date = list(d.loc["Document Period End Date"])
        for d in date: 
            try:
                dt = parse(str(d).replace("\n"," ").replace("\t"," "))
                return dt.strftime('%Y-%m-%d')

            except:
                continue
            
        # dt = parse(str(date))
        # return dt.strftime('%Y-%m-%d')
        if dt == None:
            dt = parse(str(date))

    def parse_raw_df(self,
                     df,
                     type : str):
        # check date exists #
        if (self.temp_date == None):
            print("no date is in temp_date variable")
            return

        # check correct type
        assert (type in [INCOME, BALANCE, CASHFLOW]), print(
            "when parsing raw DF - must give correct type: income, balance, cashflow")

        # first get multipler
        multiplier = self.get_multiplier(df)


        first_row = df.iloc[0].tolist()

        # deal with df where 'x Months End' exists in
        if (self.months_in_header(first_row)):
            df = self.fix_monthes_in_header(df)

        # find out which colums share the same date as the document date
        # if there are more than one make sure to grab the correct one
        df = df.replace("\t","").replace("\n","")
        date_positions = []
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                try:
                    dt = parse(str(df.iat[i,j]))
                    dt = dt.strftime('%Y-%m-%d')
                    if (str(dt) == str(self.temp_date)):
                        date_positions.append((i,j))
                        # print(dt)
                        # print("index = ",i, "col = ", j)

                except:
                    pass

        if len(date_positions) != 1:
            print("Found more than 1 occurance of ", self.temp_date, "in df: ", df.head())
        else:
            new_df = df.iloc[:,[0,date_positions[0][1]]]
            # print(new_df)



        if (type == INCOME):
            pass
        elif (type == BALANCE):
            self.temp_b_s = new_df
        else:
            pass

    def get_multiplier(self, df): ## TODO - reutrn both $, stock multipliers
        mulitpler = df.iloc[0,0].lower().split("$")
        shares_multy  = 1
        numeric_multy = 1
        
        for candidate in mulitpler:
            if ("share" not in candidate):
                if ("thousand" in candidate):
                    numeric_multy = THOUSNADS
                elif ("million" in candidate):
                    numeric_multy = MILLIONS
                elif ("billion" in candidate):
                    numeric_multy = BILLIONS
            else:
                if ("thousand" in candidate):
                    shares_multy = THOUSNADS
                elif ("million" in candidate):
                    shares_multy = MILLIONS
                elif ("billion" in candidate):
                    shares_multy = BILLIONS
                

        # print("Could not find the multipler for ", self.ticker)
        return (numeric_multy, shares_multy)

    def months_in_header(self, l : list):
        if len(l) == 0:
            print("Len of header in df is 0!")
            return None
        for i in l:
            if (type(i) == str and "months" in i.lower()):
                return True
        return False

    def fix_monthes_in_header(self, df):
        first_row = df.iloc[0].tolist()
        new_row   = first_row
        temp_var = None
        for i in range(len(first_row)):
            temp_tag = first_row[i]
            if (pd.isna(temp_tag) == False and "months" in str(temp_tag).lower()):
                temp_var = temp_tag
            elif(pd.isna(temp_tag) == True and temp_var != None):
                new_row[i] = temp_var

        df.iloc[0] = new_row

        d = dict(zip(df.columns, range(len(df.columns))))
        s = df.rename(columns=d).stack()
        nine_months_coors = s[(s == '9 Months Ended')].index.tolist()
        for i in reversed(nine_months_coors):
            df = df.drop(columns = i[1])

        d = dict(zip(df.columns, range(len(df.columns))))
        s = df.rename(columns=d).stack()
        six_months_coors  = s[(s == '6 Months Ended')].index.tolist()
        for i in reversed(six_months_coors):
            df = df.drop(columns = i[1])

        return df

    def prase_balance_sheet(self):
        
        def update_dic(df_to_iterate: pd.DataFrame,
                       original_dic : dict,
                       _type         : str,
                       date):
            temp_d = original_dic
            for row_idx in range(len(df_to_iterate.index)):
                tag,val = df_to_iterate.iloc[row_idx,0].lower(), df_to_iterate.iloc[row_idx,1]
                if (not pd.isna(val)):
                    tag = statements_templates.convert_naming_convention(tag, _type)
                    if (tag != ""):
                        original_dic = _utils.add_data_to_statement(key = tag, d = original_dic, data_to_write = {date:val})

            
            return original_dic
        
        if(self.temp_b_s.empty):
            print("Balance sheet of {} is empty DF".format(self.ticker))
            return

        multiplier = self.get_multiplier(self.temp_b_s)

        # divide into sections
        current_assets_idx      = non_current_assetes_idx     = None
        current_liabilities_idx = non_current_liabilities_idx = None
        equity_idx              = None
        
        title_row = total_row = None
        
        # current assetes:
        for row_idx in range(len(self.temp_b_s.index)):
            tag,val = self.temp_b_s.iloc[row_idx,0].lower(), self.temp_b_s.iloc[row_idx,1]
            tag = tag.replace(":", "").replace("-", " ")
            if ("current" in tag and "assets" in tag and pd.isna(val)):
                title_row = row_idx
            if ("total" in tag and "assets" in tag and not pd.isna(val)):
                total_row = row_idx
                if (title_row == None):
                    print("ERROR")
                else:
                    current_assets_idx = {TITLE_ROW:title_row, TOTAL_ROW:total_row}
                    break

        non_current_assetes_idx = {TITLE_ROW:total_row + 1}

        # non current assetes
        for row_idx in range(total_row + 1, len(self.temp_b_s.index)):
            tag,val = self.temp_b_s.iloc[row_idx,0].lower(), self.temp_b_s.iloc[row_idx,1]
            tag = tag.replace(":", "").replace("-", " ")
            if (("total" in tag and "assets" in tag and not pd.isna(val))):
                total_row = row_idx
                non_current_assetes_idx[TOTAL_ROW] = total_row
            elif ("liabilities" in tag):
                total_row = row_idx - 1
                non_current_assetes_idx[TOTAL_ROW] = total_row
                break

        current_liabilities_idx = {TITLE_ROW: total_row + 1}

        # current liabilties
        for row_idx in range(total_row + 1, len(self.temp_b_s.index)):
            tag, val = self.temp_b_s.iloc[row_idx, 0].lower(), self.temp_b_s.iloc[row_idx, 1]
            tag = tag.replace(":", "").replace("-", " ")
            if ("current" in tag and "liabilities" in tag and pd.isna(val)):
                current_liabilities_idx = {TITLE_ROW:row_idx}
            if ("total" in tag and "liabilities" in tag and not pd.isna(val)):
                current_liabilities_idx[TOTAL_ROW] = row_idx
                break
            elif ("equity" in tag):
                current_liabilities_idx[TOTAL_ROW] = row_idx - 1
                break

        # non current liabilties
        non_current_liabilities_idx = {TITLE_ROW: row_idx + 1}
        for row_idx in range(row_idx + 1, len(self.temp_b_s.index)):
            tag,val = self.temp_b_s.iloc[row_idx,0].lower(), self.temp_b_s.iloc[row_idx,1]
            tag = tag.replace(":", "").replace("-", " ")
            if (("total" in tag and "liabilities" in tag and not pd.isna(val))):
                total_row = row_idx
                non_current_liabilities_idx[TOTAL_ROW] = total_row
                break
            
        # equity index
        equity_idx = {TITLE_ROW: row_idx + 1, TOTAL_ROW : len(self.temp_b_s.index)}        


        


        # check that all idxes make sense:
        idxs_list = [current_assets_idx, non_current_assetes_idx,current_liabilities_idx,non_current_liabilities_idx, equity_idx]
        for idx in idxs_list:
            if (idx == None):
                print("ERROR: could not parse {} balance sheet - did not found idxes".format(self.ticker))
                return
            if (len(idx) != 2):
                print("ERROR: parsing balance - did not find a whole pair of idxes for {}".format(self.ticker))
                return

            if (idx[TITLE_ROW] == idx[TOTAL_ROW]):
                print("ERROR: parsed {} balance sheet - and used the same index {}".format(self.ticker, idx[TITLE_ROW]))
                return

        assets_df              = self.temp_b_s.iloc[current_assets_idx[TITLE_ROW]:non_current_assetes_idx[TOTAL_ROW] + 1]
        liablities_df          = self.temp_b_s.iloc[current_liabilities_idx[TITLE_ROW]:non_current_liabilities_idx[TOTAL_ROW] + 1]
        current_assets_df      = self.temp_b_s.iloc[current_assets_idx[TITLE_ROW]:current_assets_idx[TOTAL_ROW] + 1]
        current_liabilities_df = self.temp_b_s.iloc[current_liabilities_idx[TITLE_ROW]:current_liabilities_idx[TOTAL_ROW] + 1]
        non_current_assets_df  = self.temp_b_s.iloc[non_current_assetes_idx[TITLE_ROW]:non_current_assetes_idx[TOTAL_ROW] + 1]
        non_current_liablities_df = self.temp_b_s.iloc[non_current_liabilities_idx[TITLE_ROW]:non_current_liabilities_idx[TOTAL_ROW] + 1]
        equity_df                 = self.temp_b_s.iloc[equity_idx[TITLE_ROW]:equity_idx[TOTAL_ROW] + 1]
        


        # current assets
        self.comp_data[BALANCE] = update_dic(current_assets_df, self.comp_data[BALANCE], statements_templates.ASSETS_ST, self.temp_date)
        
        # non current assets
        self.comp_data[BALANCE] = update_dic(non_current_assets_df, self.comp_data[BALANCE], statements_templates.ASSETS_LT, self.temp_date)
        
        # current liabilties
        self.comp_data[BALANCE] = update_dic(current_liabilities_df, self.comp_data[BALANCE], statements_templates.LIABILATIES_ST, self.temp_date)
        
        # non current liablities
        self.comp_data[BALANCE] = update_dic(non_current_liablities_df, self.comp_data[BALANCE], statements_templates.LIABILATIES_LT, self.temp_date)

        # equity
        self.comp_data[BALANCE] = update_dic(equity_df, self.comp_data[BALANCE], statements_templates.EQUITY, self.temp_date)
        
        # update local pickle copy
        self.update_local_pkl(self.comp_data)
        





    def convert_general_to_template(self,
                                    df   : pd.DataFrame,
                                    type : str):
        # create a temporary balance sheet from template
        temp_bs = statements_templates.BALANCE_SHEET_TEMPLATE

        if (self.check_type(type) and not df.empty):

            if (type == INCOME):
                pass # TODO

            elif (type == BALANCE):
                self.prase_balance_sheet()

            else:
                pass # TODO

        else:
            return



    def add_data_to_main(self,
                         df : pd.DataFrame,
                         type : str):
        for row_idx in len(range(df.index)):
            tag, val = df.iloc[row_idx, 0].lower(), df.iloc[row_idx, 1]
            tag = statements_templates.find_best_matach_group(input = tag, type = type)
        return


    def work(self):
        self.get_comp_db(self.ticker)
        self.get_temp_sheets()
        self.parse_raw_df(self.temp_b_s, BALANCE)
        self.convert_general_to_template(self.temp_b_s, BALANCE)

    def check_type(self, type : str):
        if type not in [BALANCE, INCOME, CASHFLOW]:
            print("ERROR: only types: " + ",".join([BALANCE, INCOME, CASHFLOW], " are allowed - got : ", type))
            return False
        return True


# =============================================================================
# C = comp_data_handler_c("MMM")
# C.get_comp_db("MMM")
# C.get_temp_sheets()
# C.parse_raw_df(C.temp_b_s, BALANCE)
# C.convert_general_to_template(C.temp_b_s, BALANCE)
# # C.prase_balance_sheet()
# # C.get_comp_db("MMM")
# =============================================================================


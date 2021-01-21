from Lib.src.cfg import *


### Consts ###
test_f = "C:/Users/avsha/Downloads/Balance Sheet_Annual_As Originally ReportedMMM.xls"
##############



class Comp_analysis_c:
    def __init__(self,
                 ticker):

        self.ticker = ticker
        self.db     = self.get_db()

    def get_db(self):
        d = pd.read_excel(test_f, index_col = 0)
        return d

    def calc_operational_balance(self):

        def clear_financial_assets_liab(balance_sheet : pd.DataFrame):
            data = balance_sheet
            tags = data.index
            c = 0
            while "liab" not in tags[c].lower():
                print(tags[c])
                c += 1
            return


        """
        
        :return: 
        """

        """
        divide balance sheet to 3 parts:
        1) financial assetes
        2) extra assets
        3) operational assetes
        ----------------------
        on the other side of the balance:
        1) financial debt
        2) equaty
        ---------------------
        we want to clear the picture and use only extra + operational asseets - this means reducing financial assets
        
        """
        clear_financial_assets_liab(self.db)
        return

comp = Comp_analysis_c("asd")
comp.calc_operational_balance()
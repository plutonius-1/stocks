from Lib.src.cfg import HTML_LINK_TYPE, TEMP_COMPANIES_INDEX_NAME
from Lib.src.cfg import *
from Lib.src.utils import *
import xlsx_parser_c
import Lib.src.comp_data_handler_c as comp_data_handler

#todo - change prints to work with std_err
class requestst_handler_c:
    def __init__(self):
        self.sec_companies_index = SEC_ARCHIVE_COMPANIES_INDEX
        self.xlsx_parser         = xlsx_parser_c
        self.idx_file_search_pat = ""
        self.comp_data_handler   = comp_data_handler()

    def get_cik(self, ticker):
        results = CIK_RE.findall(reqs.get(URL.format(ticker)).text)
        if len(results) == 0:
            print("Coulnd't find CIK for: ", ticker)
            return None

        cik = results[0]

        for i in results:
            if (i != cik):
                print("Found differernt CIKs for the same tickre: {} : {}".format(ticker, results))
                return None
        return cik


    def get_xlsx_file(self,
                      company_data_path : str
                      ):
        req  = reqs.get(company_data_path + "/" + FINANCIAL_REPORT_POSTFIX)
        if (req.status_code != reqs.codes.ok):
            print("requested page: {} - unsuccesful!", company_data_path)
            return None

        output = open(TEMP_XLSX_FILE_NAME, 'wb')
        output.write(req.content)
        output.close()
        return

    def parse_idx_file(self,
                       idx_file,
                       ticker : str):

        tmp_line = None

        # sanity check
        if (idx_file == None):
            print("cannot parese idx_file - it is NONE")
            return

        # get CIK
        cik = self.get_cik(ticker)
        cik = str(cik).lstrip("0")

        f = open(TEMP_COMPANIES_INDEX_NAME, "r")
        lines = f.readlines()
        for l in lines:
            # first look for the 10-K,10-Q
            if (("10-K" in l or "10-Q" in l) and (cik in l)):
                data_path = re.search("edgar.*txt", l) ## TODO
                if (data_path == None):
                    print("Could not find a data path within idx file ")
                    return None
                else:
                    tmp_line = data_path.group(0).replace("-","").replace(".txt","")

        if (tmp_line == None):
            print("did not find {} in idx file - try rewriting".format(ticker))
        return tmp_line

    def get_idx_path(self,
                      qtr_url : str
                      ):
        qtr_page = reqs.get(qtr_url)
        soup = BeautifulSoup(qtr_page.text, "html.parser")
        idx_file = soup.find(HTML_LINK_TYPE, attrs={'href': "company.idx"})
        idx_file_path = qtr_url + idx_file.get("href");
        idx_file = reqs.get(idx_file_path)
        return idx_file


    def get_year_data(self,
                      ticker : str,
                      year : int):
        year_url  = self.sec_companies_index + str(year) + URL_POSTFIX
        year_page = reqs.get(year_url)

        #sanity check
        if (year_page.status_code != reqs.codes.ok):
            print("requests_handler - did not find a year {} page".format(year))
            return None

        else:
            soup = BeautifulSoup(year_page.text, 'html.parser')
            table = soup.find_all("table")

            if (len(table) != 1):
                print("requests_handler - found more than 1 table in year page")

            else:
                for link in table[0].find_all(HTML_LINK_TYPE):
                    qtr_url  = year_url + link.get(HTML_HREF_TYPE)
                    idx_file = open(TEMP_COMPANIES_INDEX_NAME, WRITE)
                    idx_file.write(self.get_idx_path(qtr_url).text)
                    idx_file.close()

                    company_data_path = self.parse_idx_file(idx_file, ticker)

                    # download the excel file
                    self.get_xlsx_file(SEC_ARCHIVE_BASE + company_data_path)

                    # let the comp_data_handler prase the data and add to DB
                    self.comp_data_handler


                    # remove after use
                    os.remove(TEMP_COMPANIES_INDEX_NAME)
        return

    def get_data_all(self):

        base_page = reqs.get(self.sec_companies_index)
        soup = BeautifulSoup(base_page.text, 'html.parser')
        return



rh = requestst_handler_c()
rh.get_year_data("mmm", 2019)
# print(rh.get_cik("mmm"))


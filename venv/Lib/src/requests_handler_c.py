from Lib.src.cfg import HTML_LINK_TYPE, TEMP_COMPANIES_INDEX_NAME
from Lib.src.cfg import *
from Lib.src.utils import *
import Lib.src.comp_data_handler_c 

#todo - change prints to work with std_err
class requestst_handler_c:
    def __init__(self):
        self.sec_companies_index = SEC_ARCHIVE_COMPANIES_INDEX
        self.idx_file_search_pat = ""
        self._comp_data_handler  = None

    def get_cik(self, ticker):
        results = CIK_RE.findall(reqs.get(CIK_URL.format(ticker)).text)
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

    def get_idx_file(self, year, ticker):
        """
        use this function in case 'prase_idx_file' does not produce the direct link
        
        """
        
        URL = SEC_ARCHIVE_COMPANIES_INDEX
        year_ = str(year) + "/"
        
        quaeters_page = reqs.get(URL + year_)
        if (quaeters_page.status_code != 200):
            print("Did not find: ", URL + year_)
            return 
        
        
        soup = BeautifulSoup(quaeters_page.text, HTML_PARSER)
        table = soup.find_all("table")

        if (len(table) != 1):
            print("requests_handler - found more than 1 table in year page")

        else:
           for link in table[0].find_all(HTML_LINK_TYPE):
               idx_path  = URL + year_ + link.get(HTML_HREF_TYPE) + "/company.idx" ## TODO
               idx_page = reqs.get(idx_path)
               
               idx_file = open(TEMP_COMPANIES_INDEX_NAME, WRITE)
               idx_file.write(idx_page.text)
               idx_file.close()
        
        
        return
    
    
    def parse_all_idx_files(self, ticker):
        
        
        def find_urls_in_idx_file(idx_file, cik):
            xlsx_files_paths = []
            
            
            lines = idx_file.readlines()
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
                        else:
                            xlsx_files_paths.append(tmp_line)
            return xlsx_files_paths
                        

           
        # get CIK
        cik = self.get_cik(ticker)
        cik = str(cik).lstrip("0")
        # print("CIK = ", cik)
        
        xlsx_files_paths = []
        
        tmp_line = None
        
        idx_files = sorted([i for i in os.listdir("./") if TEMP_COMPANIES_QTR_INDEX_NAME in i])
        
        if (len(idx_files) > 4):
            print("too many idx fiels in local dir")
            return
            
        if (len(idx_files)) < 1:
            print("not enough idx files in local dir")
            return
        
        for file in idx_files:
            idx_file = open("./"+file, READ)
            temp_xlsx_files_paths = find_urls_in_idx_file(idx_file, cik)
            
            xlsx_files_paths += temp_xlsx_files_paths
        
        for file in idx_files:
            os.remove("./" + file)
        
        return xlsx_files_paths
    
    
    
    
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
        print("found idx from: ", qtr_url)
        return idx_file


    def get_year_data(self,
                      ticker : str,
                      year : int):
        year_url  = self.sec_companies_index + str(year) + URL_POSTFIX
        year_page = reqs.get(year_url)
        
        # make sure ticker is capital
        ticker = ticker.upper()

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
                # for link in table[0].find_all(HTML_LINK_TYPE):
                self.get_all_idxs_files(year)
                for link in self.parse_all_idx_files(ticker):
                    # qtr_url  = year_url + link.get(HTML_HREF_TYPE)
                    # idx_file = open(TEMP_COMPANIES_INDEX_NAME, WRITE)
                    # idx_file.write(self.get_idx_path(qtr_url).text)
                    # idx_file.close()

                    # company_data_path = self.parse_idx_file(idx_file, ticker)

                    # download the excel file
                    self.get_xlsx_file(SEC_ARCHIVE_BASE + link)

                    # let the comp_data_handler prase the data and add to DB
                    self._comp_data_handler = comp_data_handler_c(ticker)
                    self._comp_data_handler.work()


                    # remove after use
                    #os.remove(TEMP_COMPANIES_INDEX_NAME)
                print("Done parsing {}'s - year: {}".format(ticker, year))
        return

    def get_data_all(self):

        base_page = reqs.get(self.sec_companies_index)
        soup = BeautifulSoup(base_page.text, 'html.parser')
        return

    
    def get_all_idxs_files(self, year):
        
        
        URL = SEC_ARCHIVE_COMPANIES_INDEX
        year_ = str(year) + "/"
        
        quarters_page = reqs.get(URL + year_)
        if (quarters_page.status_code != 200):
            print("Did not find: ", URL + year_)
            return         
        
        soup = BeautifulSoup(quarters_page.text, HTML_PARSER)
        table = soup.find_all("table")

        if (len(table) != 1):
            print("requests_handler - found more than 1 table in year page")

        else:
           qtr_count = 1
           for link in table[0].find_all(HTML_LINK_TYPE):
               idx_path  = URL + year_ + link.get(HTML_HREF_TYPE) + "/company.idx" ## TODO
               idx_page = reqs.get(idx_path)
               idx_file = open(TEMP_COMPANIES_QTR_INDEX_NAME + "_" + str(qtr_count) + TEMP_IDX_FILE_TYPE, WRITE)
               idx_file.write(idx_page.text)
               idx_file.close()
               qtr_count += 1       
        return

rh = requestst_handler_c()
rh.get_year_data("AAPL", 2019)
# rh.get_all_idxs_files(2019)
# rh.parse_all_idx_files("GME")
# print(rh.get_cik("GME"))


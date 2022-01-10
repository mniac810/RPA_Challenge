from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem

from open_agencies import OpenAgencies
from open_website import OpenWebsite
from excel_maker import ExcelMaker
from get_individual_investment import GetIndividualInvestment
from pdf_downloader import PDFDownloader

import os


class ITRobot:

    def __init__(self):
        self.agencies_list = OpenAgencies()
        self.individual_agencies = GetIndividualInvestment('422')

    def _pdf_download(self, investments_table):
        browser = Selenium()
        files = FileSystem()

        
        dir = f'{os.getcwd()}/output'
        links = [investment['link'] for investment in investments_table if investment['link']]
        names = [investment['UII'] for investment in investments_table if investment['link']]


        browser.set_download_directory(dir, True)
        num=0
        for link in links:
            if link != '':
                browser.open_available_browser(link)            
                browser.wait_until_element_is_visible('//*[@href="#"]')
                browser.click_element('//*[@href="#"]')
                while files.does_file_not_exist(
                        '{}/{}.pdf'.format(dir, names[num])):
                    continue     
            num += 1

    def run(self):
        self.agencies_list.open_and_click()
        list_agencies = self.agencies_list.parse()
        
        maker = ExcelMaker(
            content = list_agencies, 
            name = 'Agencies',
            path = 'output/agencies.xlsx',
            exclude_keys='link'
        )

        maker.set_content()

        workbook = maker.get_workbook()
        investments_table = self.individual_agencies.parse()

        maker = ExcelMaker(
            content=investments_table,
            name='IndividualInvestments',
            path='output/agencies.xlsx',
            workbook=workbook,
            exclude_keys='link'
        )

        self._pdf_download(investments_table)

        maker.set_content()
        maker.save_workbook()
        maker.close()



        

        
if __name__ == "__main__":
    robot = ITRobot()
    robot.run()

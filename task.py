from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem

from open_agencies import OpenAgencies
from excel_maker import ExcelMaker
from get_individual_investment import GetIndividualInvestment
from pdf_downloader import PDFDownloader

import os


class ITRobot:

    def __init__(self):
        self.agencies_list = OpenAgencies()
        self.individual_agencies = GetIndividualInvestment('422')
        self.browser = Selenium()
        self.files = FileSystem()

    def run(self):
        list_agencies = self.agencies_list.parse()

        agencies_maker = ExcelMaker(content=list_agencies,
                                    name='Agencies',
                                    path='output/agencies.xlsx',
                                    exclude_keys='link')

        agencies_maker.set_content()

        workbook = agencies_maker.get_workbook()
        investments_table = self.individual_agencies.parse()

        individual_investment_maker = ExcelMaker(content=investments_table,
                                                 name='IndividualInvestments',
                                                 path='output/agencies.xlsx',
                                                 workbook=workbook,
                                                 exclude_keys='link')

        dir = f'{os.getcwd()}/output'
        links = [
            investment['link'] for investment in investments_table
            if investment['link']
        ]
        names = [
            investment['UII'] for investment in investments_table
            if investment['link']
        ]
        self.browser.set_download_directory(dir, True)
        downloader = PDFDownloader(links, names)
        downloader.pdf_download()

        individual_investment_maker.set_content()
        individual_investment_maker.save_workbook()
        individual_investment_maker.close()


if __name__ == "__main__":
    robot = ITRobot()
    robot.run()

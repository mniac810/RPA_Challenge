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
        # Medium: create another variable for the new ExcelMaker. It is a bad practice to override variable like this
        maker = ExcelMaker(
            content=investments_table,
            name='IndividualInvestments',
            path='output/agencies.xlsx',
            workbook=workbook,
            exclude_keys='link'
        )

        maker.set_content()
        maker.save_workbook()
        maker.close()


        # Critical: Remove comment 
        # print(links)
        # for link in links:
        #     downloader = PDFDownloader(link)
        #     downloader.download_pdf()

        dir = f'{os.getcwd()}/output'
        links = [investment['link'] for investment in investments_table if investment['link']]
        names = [investment['UII'] for investment in investments_table if investment['link']]
        
        # Medium: I believe is it better to put this into __init__
        browser = Selenium()
        files = FileSystem()


        browser.set_download_directory(dir, True)
        num=0
        for link in links:
            if link != '':
                browser.open_available_browser(link)
                # Click to download
                browser.wait_until_element_is_visible('//*[@href="#"]')
                browser.click_element('//*[@href="#"]')
                # Wait for completed downloads
                while files.does_file_not_exist(
                        '{}/{}.pdf'.format(dir, names[num])):
                    continue     
            num += 1

        
if __name__ == "__main__":
    robot = ITRobot()
    robot.run()

from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem

import datetime
import os


class PDFDownloader:

    def __init__(self, page_url):
        self.browser = Selenium()
        self.files = FileSystem()
        self._url = page_url
        print(self._url)

    def _wait_download(self, name):
        while self.files.does_file_not_exist('{}/output/{}.pdf'.format(
                os.getcwd(), name)):
            continue

    def download_pdf(self):
        self.browser.set_download_directory('{}/output'.format(os.getcwd),
                                            True)

        self.browser.open_available_browser(self._url)
        self.browser.wait_until_element_is_visible(
            locator="css:div#business-case-pdf>a",
            timeout=datetime.timedelta(minutes=1))
        self.browser.click_element(locator="css:div#business-case-pdf>a")
        self._wait_download(self._url.split('/')[-1])
        self.browser.close_browser()

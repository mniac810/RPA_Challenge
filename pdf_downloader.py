from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem

import datetime
import os


class PDFDownloader:

    def __init__(self, page_urls, names):
        self.browser = Selenium()
        self.files = FileSystem()
        self._dir = f'{os.getcwd()}/output'
        self._urls = page_urls
        self._names = names

    def pdf_download(self):
        dir = f'{os.getcwd()}/output'

        self.browser.set_download_directory(dir, True)

        for num, url in enumerate(self._urls):
            self.browser.open_available_browser(url)
            self.browser.wait_until_element_is_visible(
                locator="css:div#business-case-pdf>a",
                timeout=datetime.timedelta(minutes=1))
            self.browser.click_element(locator="css:div#business-case-pdf>a")
            self.files.wait_until_created('{}/{}.pdf'.format(
                dir, self._names[num]),
                                          timeout=60.0 * 5)
            self.browser.close_browser()

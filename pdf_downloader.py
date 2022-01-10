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

    # Medium: I am confused by your naming convention. Is is a written Python convention (i dont write Python that often)?
    # Or else please be consistent whether or not to have a _ at the start of method name
    def _wait_download(self, name):
    # Critical: this while loop here is very bad. It can potentially be a blocking thread if the file can never be download. You will need a timeout
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

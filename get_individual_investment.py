from RPA.Browser.Selenium import Selenium
from pdf_downloader import PDFDownloader

import datetime


class GetIndividualInvestment:
  BASE_URL = "https://itdashboard.gov/drupal/summary/{}"

  def __init__(self, agency_id):
    self._link = self.BASE_URL.format(agency_id)
    self.browser = Selenium()
    self.browser.open_available_browser(self._link)

  def _get_table(self):
    self.browser.wait_until_element_is_visible(
      locator='css:div#investments-table-widget div.pageSelect select option:nth-of-type(4)',
      timeout=datetime.timedelta(minutes=1)
    )
    self.browser.click_element(
        locator='css:div#investments-table-widget div.pageSelect select option:last-of-type'
    )
    self.browser.wait_until_element_is_visible(
        locator='css:div#investments-table-widget table#investments-table-object tbody tr:nth-of-type(11) td',
        timeout=datetime.timedelta(minutes=1)
    )
    agencies = self.browser.get_webelement(
        locator='css:div#investments-table-widget'
    )
    return agencies

  def _get_header(self, table):
    self.browser.wait_until_element_is_visible(
      locator=[table, 'css:div.dataTables_scrollHead table th'],
      timeout=datetime.timedelta(minutes=1)
    )
    headers = self.browser.get_webelements(locator=[table, 'css:div.dataTables_scrollHead table th'])
    return [header.text for header in headers]

  def _get_rows(self, table):
    self.browser.wait_until_element_is_enabled(locator=[table, 'css:table#investments-table-object tbody tr'])
    rows = self.browser.get_webelements(locator=[table, 'css:table#investments-table-object tbody tr'])
    return rows

  def _get_cells(self, rows):
    cells = self.browser.get_webelements(locator=[rows, 'css:td'])
    return cells

  def parse(self):
    table = self._get_table()
    headers = self._get_header(table = table)
    rows = self._get_rows(table = table)
    investments = []

    self.browser.wait_until_element_is_visible(
      locator=[table, 'css:table#investments-table-object tbody tr td a'],
      timeout=datetime.timedelta(seconds=10)
    )

    for row in rows:
      investment = {}
      cells = self._get_cells(row)
      for num, cell in enumerate(cells):
        investment[headers[num]] = cell.text
        
        if num == 0:
          count_link = self.browser.get_element_count(
            locator=[cell, 'css:a']
          )
          if count_link > 0:
            investment['link'] = self.browser.get_element_attribute(
              locator=[cell, 'css:a'],
              attribute = 'href'
            )
          else:
            investment['link'] = ''

      investments.append(investment)

    return investments


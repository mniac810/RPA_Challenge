from RPA.Browser.Selenium import Selenium


class OpenWebsite:

  def __init__(self, url, button):
    self.url = url
    self.button = button
    self.browser = Selenium()

  def store_screenshot(self,filename):
    self.browser.screenshot(filename=filename)

  def open(self):
    self.browser.open_available_browser(self.url)

  def wait_until_element_visible(self, locator):
    while not self.browser.is_element_visible(locator):
        continue

  def click_dive_in(self):
    self.wait_until_element_visible(self.button)
    self.browser.click_element(self.button)
    self.store_screenshot("output/screenshot.png")
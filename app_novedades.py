import os
import re
import unittest

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

from helpers.helper import pdf_downloader
from pyunitreport import HTMLTestRunner

load_dotenv()

class App(unittest.TestCase):
    
    def setUp(self):
        """
        Set up the webdriver with specified options and an implicit wait time of 10 seconds.
        The webdriver is created using the Chrome driver executable file path specified by the environment variable "path_chrome".
        The options set for the Chrome webdriver include starting the browser maximized.
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized") # Inicia el navegador maximizado
        self.driver = webdriver.Chrome(os.getenv("path_chrome"),options=options)
        self.driver.implicitly_wait(10)


    def test_run(self):
        """
        Test method that navigates to a specified website, finds certain elements on the page, and downloads PDF files.
        
        This method performs the following steps:
        1. Navigates to a website specified by the environment variable "url".
        2. Finds and clicks on an element on the page with the text "Noveda".
        3. Collects the URL of the current page and stores it in a list called "urls".
        4. Collects additional URLs from pagination links on the page, and appends them to the "urls" list.
        5. Calls the "get_urls" method for each URL in the "urls" list and appends the resulting PDF URLs to a list called "urls_pdf".
        6. Calls the "get_pdf" method with the "urls_pdf" list to download the PDF files.
        """
        driver = self.driver

        driver.get(os.getenv("url"))
        arrivals = driver.find_element(By.XPATH, '//a[contains(text(), "Noveda")]')
        arrivals.click()

        urls = [driver.current_url] 
        urls_pdf = []

        pagination = driver.find_elements(By.XPATH, '//ul[@class="pagination pagination"]/li[not(@class="prev disabled") and not(@class="next")]/a')
        for pag in pagination:
            url_pag = pag.get_attribute("href")
            urls.append(url_pag)
    
        for i in urls:
            urls_pdf += (self.get_urls(i))

        self.get_pdf(urls_pdf)



    def get_urls(self, url_pag):
        """
        Helper method to get the URLs of PDFs to download on a given webpage.

        :param url_pag: URL of the webpage to search for PDF download links.
        :type url_pag: str

        :return: A list of URLs to download PDF files from the given webpage.
        :rtype: list of str
        """
        urls = []
        driver = self.driver 
        driver.get(url_pag)
        cards_filter = driver.find_elements(By.XPATH, './/p[@class ="book__author"][contains(a/text(), "Arik Eindrok")]/..')

        for element in cards_filter :
            url = element.find_element(By.XPATH, './/li/a[contains(text(), "Descargar")]')
            url = url.get_attribute("href")
            urls.append(url)
        
        return urls


    def get_pdf(self,urls):
        """
        Downloads PDFs from a given list of URLs.

        Args:
            urls: A list of URLs of the PDFs to download.
        """
        driver = self.driver 
        urls_pdf = []

        for url in urls :
            driver.get(url)
            download = driver.find_element(By.XPATH, '//a[contains(., "PDF")]')
            download =download.get_attribute('onclick')
            url_pdf =  re.search(r"\'([^']+)\'", download).group(1)
            url_pdf = os.getenv("url") + url_pdf 
            urls_pdf.append(url_pdf)

        pdf_downloader(urls_pdf)


    def tearDown(self):
        """
        Quit the webdriver after the test has run.
        """
        self.driver.quit()


    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity = 2, testRunner = HTMLTestRunner(output = 'vorex', report_name = "logs"))
import os
import re
import unittest
from datetime import datetime

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

from helpers.helper import pdf_downloader
from pyunitreport import HTMLTestRunner

load_dotenv()


class App(unittest.TestCase):
    
    
    def setUp(self):
        
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized") # Inicia el navegador maximizado
        self.driver = webdriver.Chrome(os.getenv("path_chrome"),options=options)
        driver = self.driver
        
        driver.implicitly_wait(10)

    def test_run(self):

        driver = self.driver
        urls = []
        driver.get(os.getenv('url'))
        arrivals = driver.find_element(By.XPATH, '//section/h2[.="Novedades"]/..')
        cards_filter = arrivals.find_elements(By.XPATH, './/p[@class ="book__author"][contains(a/text(), "Arik Eindrok")]/..')

        for element in cards_filter :
            url = element.find_element(By.XPATH, './/li/a[contains(text(), "Descargar")]')
            url = url.get_attribute("href")
            urls.append(url)

        self.get_pdf(urls)
        
    
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



if __name__ == "__main__":
    unittest.main(verbosity = 2, testRunner = HTMLTestRunner(output = 'test2', report_name = "logs"))

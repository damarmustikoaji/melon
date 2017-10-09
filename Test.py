import sys
import unittest
import time
import requests
from termcolor import colored
from selenium import webdriver

class CheckLinksTest(unittest.TestCase):

    SERVER = None
    EMAIL = None

    @classmethod
    def setUpClass(cls):
        if cls.BROWSER == "Chrome":
            cls.driver = webdriver.Chrome(executable_path='../driver/chromedriver')
        elif cls.BROWSER == "PhantomJS":
            try:
                cls.driver = webdriver.PhantomJS()
            except Exception as e:
                cls.driver = webdriver.PhantomJS('../driver/phantomjs')
        elif cls.BROWSER == "Firefox":
            cls.driver = webdriver.Firefox(executable_path='../driver/geckodriver')
        elif cls.BROWSER == "Opera":
            cls.driver = webdriver.Opera(executable_path='../driver/operadriver')
        elif cls.BROWSER == "Mobile":
            mobile_emulation = {
            "deviceName": "iPhone 5"
            #"deviceName": "Nexus 5"
            }
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            cls.driver = webdriver.Chrome(executable_path='../driver/chromedriver', chrome_options=chrome_options)
        else:
            assert False, "Browser driver not found '"+cls.BROWSER+"'"
        cls.driver.set_window_size(1280, 800)

    def test_a_login(self):
        self.startTime = time.time()
        no = 0
        self.driver.get(self.SERVER)
        #link_element = self.driver.find_elements_by_xpath("//a[contains(@href,'htt')]")
        r = requests.get(self.SERVER)
        if r.status_code == 200:
            status_code = colored(r.status_code, 'green')
        else:
            status_code = colored(r.status_code, 'red')
        print no, status_code, self.SERVER

        link_element = self.driver.find_elements_by_tag_name("a")
        for link in link_element:
            try:
                r = requests.get(link.get_attribute('href'))
                status_code = r.status_code
            except Exception as e:
                status_code = "NotURL"
            #time.sleep(2)
            no = no + 1
            #print no, status_code, link.get_attribute('href')
            if status_code == 200:
                status_code = colored(status_code, 'green')
            else:
                status_code = colored(status_code, 'red')
            print no, status_code, link.text, link.get_attribute('href')
        count = len(link_element)
        print "result:", count, "links"
        t = time.time() - self.startTime
        print "%s: %.3f" % (self.id(), t)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == '__main__':
    command = len(sys.argv)
    if command == 3:
        CheckLinksTest.BROWSER = sys.argv.pop()
        CheckLinksTest.SERVER = sys.argv.pop()
    else:
        sys.exit("ERROR : Please check again your argument")
    suite = unittest.TestLoader().loadTestsFromTestCase(CheckLinksTest)
    unittest.TextTestRunner(verbosity=0).run(suite)

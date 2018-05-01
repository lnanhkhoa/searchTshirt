
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import proxy_list

class FunctionsWebDriver():

    def __init__(self, selectBrowser):
        self.selectBrowser = selectBrowser
        self.webdriver = webdriver.Firefox()

    def login(self, accountFacebook):
        print("Opened facebook")
        username_box = self.webdriver.find_element_by_id('email')
        username_box.send_keys(accountFacebook.username)
        print("Email Id entered")
        time.sleep(1)
        password_box = self.webdriver.find_element_by_id('pass')
        password_box.send_keys(accountFacebook.password)
        print("Password entered")
        login_box = self.webdriver.find_element_by_id('loginbutton')
        login_box.click()
        print("Done")
        return True

    def logout(self):
        return True

    def getURL(self,url):
        return self.webdriver.get(url)

    def quit(self):
        self.webdriver.quit()

    def getWebDriver(self):
        return self.webdriver

    def changeProxy(self, ProxyHost, ProxyPort):
        "Define Firefox Profile with you ProxyHost and ProxyPort"
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", ProxyHost)
        profile.set_preference("network.proxy.http_port", int(ProxyPort))
        profile.set_preference("network.proxy.ssl", ProxyHost)
        profile.set_preference("network.proxy.ssl_port", int(ProxyPort))
        profile.update_preferences()
        return webdriver.Firefox(firefox_profile=profile)

    def fixProxy(self):
        # ""Reset Firefox Profile""
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 0)
        return webdriver.Firefox(firefox_profile=profile)

    def loadAllPostSearch(self):
        searchPage = self.webdriver.find_element_by_tag_name('html')
        stopSendKey = False
        count = 100
        while not stopSendKey or count<1:
            count -= 1
            searchPage.send_keys(Keys.END)
            time.sleep(2)
            try:
                endOfResultsElement = searchPage.find_element_by_id('browse_end_of_results_footer')
                stopSendKey = True
            except NoSuchElementException as e:
                pass

    def test(self):
        pass
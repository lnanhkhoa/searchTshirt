
import time
from selenium import webdriver
from selenium.webdriver import FirefoxProfile, DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import NoSuchElementException
import proxy_list

class FunctionsWebDriver():

    def __init__(self, selectBrowser):
        self.selectBrowser = selectBrowser
        profile = FirefoxProfile()
        profile.set_preference("permissions.default.desktop-notification", 1)
        profile.update_preferences()
        self.webdriver = webdriver.Firefox(firefox_profile=profile)

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

    def getBrowseResultContainer(self):
        BrowseResultsContainer = self.webdriver.find_element_by_id('BrowseResultsContainer')
        childsUserContentWrapper = [x for x in BrowseResultsContainer.find_elements_by_class_name('userContentWrapper')]
        for child in childsUserContentWrapper:
            contentpost = child.find_element_by_class_name('userContent')
            likeCommentContent = child.find_element_by_class_name('commentable_item')
            print (contentpost.text)
            try:
                # listImageURL = [x for x in child.find_elements_by_tag_name('img')]
                listImageURL = [x for x in child.find_elements_by_css_selector("a[rel='theater']")]
                for image in listImageURL:
                #     if image.size.get('width') > 200:
                        print( image.get_attribute('href'))
                like = likeCommentContent.find_element_by_class_name('_4arz').text
                # commentShare = likeCommentContent.find_elements_by_class_name('_36_q')
            except NoSuchElementException as e:
                like = '0'
            print ('So like :' + like)
            print('--------------------')

        # for x in range(0, len(childsUserContentWrapper)):
        #     if (x == 0):
        #         userContent = childsUserContentWrapper[0].find_elements_by_class_name('userContent')
        #         print(userContent)




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

    def clickSeeMore(self):
        listSeeMore = self.webdriver.find_elements_by_class_name('see_more_link')
        for seeMore in listSeeMore:
            seeMore.click()

    def getNameContainer(self):
        count = 0; timeout = 100
        conditionCount = True
        listNameContainer = ['BrowseResultsContainer', 'u_ps_0_3_0_browse_result_below_fold']
        while conditionCount and timeout>1:
            FindId = "fbBrowseScrollingPagerContainer" + str(count)
            timeout-=1
            try:
                self.webdriver.find_element_by_id(FindId)
                listNameContainer.append(FindId)
                count+=1
            except NoSuchElementException:
                conditionCount = False
        return listNameContainer


    def getDataContainer(self, name):
        try:
            BrowseResultsContainer = self.webdriver.find_element_by_id(name)
        except NoSuchElementException:
            return 0
        childsUserContentWrapper = BrowseResultsContainer.find_elements_by_class_name('userContentWrapper')
        for childUserContentWrapper in childsUserContentWrapper:
            print('<-------------------->')
            try:
                contentpost = childUserContentWrapper.find_element_by_class_name('userContent')
                print(contentpost.text)
            except NoSuchElementException as e:
                print(e)
                print('Empty Content')
            # Get Image URL
            listImageURL = childUserContentWrapper.find_elements_by_css_selector("a[rel='theater'][data-render-location='homepage_stream']")
            if listImageURL.__len__() == 0:
                print ('Khong co Image')
                continue
            for image in listImageURL:
                print( image.get_attribute('href'))

            text = ""
            try:
                likeCommentContent = childUserContentWrapper.find_element_by_class_name('commentable_item')
                like = likeCommentContent.find_element_by_class_name('_4arz').text
                text += like + " like, "
                commentShares = likeCommentContent.find_elements_by_class_name('_36_q')
                for commentShare in commentShares:
                    text += commentShare.text + ' ,'
                assert isinstance(like, object)
            except NoSuchElementException as e:
                text = "None like,comment,share"
            print(text)


    def test(self):
        self.webdriver.get('https://www.facebook.com/398476790565617/photos/a.398506440562652.1073741828.398476790565617/439017259844903/?type=3')
        image = self.webdriver.find_element_by_css_selector("a[rel='theater']")
        image.click()
        time.sleep(2)
        bigImage = self.webdriver.find_element_by_class_name('spotlight')
        print (bigImage.get_attribute('src'))


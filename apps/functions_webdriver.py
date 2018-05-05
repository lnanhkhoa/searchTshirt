
import time
from selenium import webdriver
from selenium.webdriver import FirefoxProfile, DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import NoSuchElementException
import proxy_list

class FunctionsWebDriver():

    def __init__(self, selectBrowser):
        self.selectBrowser = selectBrowser
        profile = FirefoxProfile()
        profile.set_preference("permissions.default.desktop-notification", 1)
        profile.update_preferences()
        self.webdriver = webdriver.Firefox(firefox_profile=profile)
        self.webdriver.maximize_window()
        self.actions = ActionChains(self.webdriver)

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

    def press_key_in_page_html(self, keypress):
        searchPage = self.webdriver.find_element_by_tag_name('html')
        searchPage.send_keys(keypress)

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
                print('Empty Content')
            # Get Image URL
            listImageURL = childUserContentWrapper.find_elements_by_css_selector(
                "a[rel='theater'][data-render-location='homepage_stream']")
            if listImageURL.__len__() == 0:
                print('Khong co Image')
                continue
            # if listImageURL.__len__() == 1:
            #     [url, likes] = self.__get_DataImageTheater__(listImageURL[0])
            #     self.press_key_in_page_html(Keys.ESCAPE)
            #     self.getLikeShareinPost(childUserContentWrapper, likes)
            #
            # if listImageURL.__len__() <4 and listImageURL.__len__()>1:
            #     for image in listImageURL:
            #         [url, likes] = self.__get_DataImageTheater__(image)
            #         self.press_key_in_page_html(Keys.ESCAPE)
            #     self.getLikeShareinPost(childUserContentWrapper)

            if listImageURL.__len__() == 1:
                arrayCheckin = []
                self.getLikeShareinPost(childUserContentWrapper)
                [url, likes] = self.__get_DataImageTheater__(listImageURL[0])
                arrayCheckin.append(url)
                conditionOutWhile = True
                count = 50
                while conditionOutWhile and count >0:
                    count -= 1
                    self.nextImageTheater()
                    newUrl = self.__get_DataNextImage__()
                    print(newUrl)
                    # check condition
                    if (newUrl in arrayCheckin):
                        conditionOutWhile = False
                    arrayCheckin.append(newUrl)
                self.press_key_in_page_html(Keys.ESCAPE)


    def getLikeShareinPost(self, childUserContentWrapper, defaultLikes = 0):
            try:
                likeCommentContentElement = childUserContentWrapper.find_element_by_class_name('commentable_item')
                textlike = self._getLikeCommentShare(likeCommentContentElement, defaultLikes)
                print(textlike)
            except NoSuchElementException as e:
                print(str(defaultLikes) + " like, comment, share")

    def test(self):
        self.webdriver.get('https://www.facebook.com/398476790565617/photos/a.398506440562652.1073741828.398476790565617/439017259844903/?type=3')
        image = self.webdriver.find_element_by_css_selector("a[rel='theater']")
        image.click()
        time.sleep(2)
        bigImage = self.webdriver.find_element_by_class_name('spotlight')
        print (bigImage.get_attribute('src'))


    def __get_numbers_in_string(self, text):
        number = [int(s) for s in text.split() if s.isdigit()]
        if len(number) == 0:
            number = [0]
        return number

    def _getLikeCommentShare(self, element, defaultLike = None):
        text = ""
        array = []
        if defaultLike == None:
            likes = element.find_elements_by_class_name('_4arz')
            for like in likes:
                text += like.text + ' likes, '
                array.extend(self.__get_numbers_in_string(like.text))
        else:
            text += str(defaultLike) + ' likes, '
            array.extend([defaultLike])
        commentShares = element.find_elements_by_class_name('_36_q')
        for commentShare in commentShares:
            text += commentShare.text + ', '
            array.extend(self.__get_numbers_in_string(commentShare.text))
        if text == "":
            text = "None like,comment,share"
        return text

    def __get_DataImageTheater__(self, image_element: object) -> object:
        wait = WebDriverWait(self.webdriver, 10)
        wait.until(EC.visibility_of(image_element))
        image_element.click()
        element = wait.until(EC.presence_of_element_located((By.ID, "photos_snowlift")))
        dropdownButton = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"fbPhotoSnowliftDropdownButton")))
        dropdownButton.click()
        imageUrlsDownload = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"a[data-action-type='download_photo']")))
        # print(imageUrlsDownload.get_attribute('href'))
        feedbackElement = wait.until(EC.presence_of_element_located((By.ID,'fbPhotoSnowliftFeedback')))
        likes = '0'
        try:
            likes = feedbackElement.find_element_by_class_name("_4arz").text
        except:
            pass
        dropdownButton.click()
        return [imageUrlsDownload.get_attribute('href'), likes]

    def __get_DataNextImage__(self):
        wait = WebDriverWait(self.webdriver, 10)
        element = wait.until(EC.presence_of_element_located((By.ID, "photos_snowlift")))
        dropdownButton = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"fbPhotoSnowliftDropdownButton")))
        dropdownButton.click()
        # 'uiContextualLayerPositioner'
        divDownloadNotHidden= wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.uiContextualLayerPositioner:not(.hidden_elem)")))
        waitDownload = WebDriverWait(divDownloadNotHidden, 10)
        imageUrlsDownload = waitDownload.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-action-type='download_photo']")))
        url = imageUrlsDownload.get_attribute('href')

        # for imageUrl in imageUrlsDownload:
        #     if imageUrl.is_displayed():
        #         url = imageUrl.get_attribute('href')
        #         print(imageUrl.get_attribute('href'))
        dropdownButton.click()
        # feedbackElement = wait.until(EC.presence_of_element_located((By.ID,'fbPhotoSnowliftFeedback')))
        # likes = '0'
        # try:
        #     likes = feedbackElement.find_element_by_class_name("_4arz").text
        # except:
        #     pass
        return url



    def escapeTheater(self, element):
        try:
            element.find_element_by_class_name("_xlt").click()
        except:
            self.press_key_in_page_html(Keys.ESCAPE)

    def nextImageTheater(self):
        wait = WebDriverWait(self.webdriver, 10)
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "next")))
        element.click()



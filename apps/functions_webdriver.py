import time, os
from selenium import webdriver
from selenium.webdriver import FirefoxProfile, DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from apps import ProcessImage
from config import DATABASE_CONFIG

# Process Image
pathImage = DATABASE_CONFIG['pathImage']
treePath = DATABASE_CONFIG['treePath']
enable_change_proxy = DATABASE_CONFIG['enable_change_proxy']
proxy_host = DATABASE_CONFIG['proxy_host']
proxy_port = DATABASE_CONFIG['proxy_port']

cur_path = os.path.dirname(__file__)
image_path_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), pathImage, treePath)
if not os.path.exists(image_path_directory):
    os.makedirs(image_path_directory)
processImage = ProcessImage(image_path_directory)
class FunctionsWebDriver:

    def __init__(self, selectBrowser, tinydbInfoAcc):
        self.selectBrowser = selectBrowser
        self.tinydbInfoAcc = tinydbInfoAcc
        self.profile: FirefoxProfile = FirefoxProfile()
        self.profile.set_preference("permissions.default.desktop-notification", 1)
        self.profile.set_preference("browser.download.folderList", 2)
        self.profile.set_preference("browser.download.manager.showWhenStarting", False)
        self.profile.set_preference("browser.download.dir", image_path_directory)
        self.profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/xml,text/plain,text/xml,"
                                                                         "image/jpeg image/png, text/csv")
        self.profile.set_preference("browser.helperApps.neverAsk.openFile","application/xml,text/plain,text/xml,"
                                                                      "image/jpeg,image/png, text/csv")
        self.profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        self.profile.set_preference("browser.download.manager.focusWhenStarting", False)
        self.profile.set_preference("browser.download.manager.useWindow", False)
        self.profile.set_preference("browser.download.manager.showAlertOnComplete", False)
        self.profile.set_preference("browser.download.manager.closeWhenDone", True)
        if enable_change_proxy:
            self.profile = self.changeProxy(proxy_host, proxy_port, self.profile)
        else:
            self.profile = self.ClearProxy(self.profile)
        self.profile.update_preferences()
        self.webdriver = webdriver.Firefox(firefox_profile=self.profile)
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

    def getURL(self, url):
        return self.webdriver.get(url)

    def quit(self):
        self.ClearProxy(self.profile)
        # self.webdriver.quit()

    def getWebDriver(self):
        return self.webdriver

    def changeProxy(self, ProxyHost, ProxyPort, profile: object = None):
        # Define Firefox Profile with you ProxyHost and ProxyPort
        if profile is None:
            profile = FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", ProxyHost)
        profile.set_preference("network.proxy.http_port", int(ProxyPort))
        profile.set_preference("network.proxy.ssl", ProxyHost)
        profile.set_preference("network.proxy.ssl_port", int(ProxyPort))
        profile.update_preferences()
        return profile

    def ClearProxy(self, profile = None):
        if profile is None:
            profile = FirefoxProfile()
        profile.set_preference("network.proxy.type", 0)
        profile.update_preferences()
        return profile

    @staticmethod
    def _get_name_in_string(string):
        array = []
        endname = string.index('?')
        for x in range(0, len(string)):
            if string[x] == '/' and x < endname:
                array.append((endname - x))
        return string[(endname - min(array) + 1):endname]

    def press_key_in_page_html(self, keypress):
        wait = WebDriverWait(self.webdriver, 10)
        searchPage = wait.until(EC.presence_of_element_located((By.TAG_NAME, "html")))
        searchPage.send_keys(keypress)

    def loadAllPostSearch(self):
        wait = WebDriverWait(self.webdriver, 10)
        searchPage = wait.until(EC.presence_of_element_located((By.TAG_NAME, "html")))
        stopSendKey = False
        count = 100
        while not stopSendKey or count < 1:
            count -= 1
            searchPage.send_keys(Keys.END)
            time.sleep(1)
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
        count = 0;
        timeout = 100
        conditionCount = True
        listNameContainer = ['BrowseResultsContainer', 'u_ps_0_3_0_browse_result_below_fold']
        while conditionCount and timeout > 1:
            FindId = "fbBrowseScrollingPagerContainer" + str(count)
            timeout -= 1
            try:
                self.webdriver.find_element_by_id(FindId)
                listNameContainer.append(FindId)
                count += 1
            except NoSuchElementException:
                conditionCount = False
        return listNameContainer

    def getMultipleDataImageTheater(self, type_script):
        if type_script == 1:
            [url, likes] = self.__get_faster_DataImageTheater__()
        else:
            [url, likes] = self.__get_DataImageTheater__()
        arrayCheckin = []
        arrayCheckin.extend(url)
        conditionOutWhile = True
        count = 50
        while conditionOutWhile and count > 0:
            count -= 1
            self.nextImageTheater()
            if type_script == 1:
                [newUrl, likes] = self.__get_faster_DataImageTheater__()
            else:
                [newUrl, likes] = self.__get_DataImageTheater__()
            # check condition
            if newUrl[0] in arrayCheckin:
                conditionOutWhile = False
            arrayCheckin.extend(newUrl)
        return [arrayCheckin, likes]

    def getDifferentDataImage(self) -> object:
        print('dac biet')
        arrayURL = []
        wait = WebDriverWait(self.webdriver, 10)
        # elementMultiImage = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='_10 _1mlf uiLayer _4-hy _3qw']")))
        allImage = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_580_")))
        for image in allImage:
            url = image.get_attribute('src')
            nameImage = self._get_name_in_string(url)
            processImage.getImageFromURL(url, nameImage)
            arrayURL.append(url)
        like = '0'
        return [arrayURL, like]

    def getLikeShareinPost(self, childUserContentWrapper, defaultLikes=0):
        try:
            likeCommentContentElement = childUserContentWrapper.find_element_by_class_name('commentable_item')
            textlike = self._getLikeCommentShare(likeCommentContentElement, defaultLikes)
            return textlike
        except NoSuchElementException as e:
            return '{0} like, comment, share'.format(str(defaultLikes))

    def __get_numbers_in_string(self, text):
        number = [int(s) for s in text.split() if s.isdigit()]
        if len(number) == 0:
            number = [0]
        return number

    def _getLikeCommentShare(self, element, defaultLike=None):
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

    def _clickFirstImageTheater_(self, image_element):
        self.webdriver.execute_script("arguments[0].scrollIntoView();", image_element)
        self.webdriver.execute_script("arguments[0].click();", image_element)
        time.sleep(1)

    def function_for_DataImageTheater(self):
        wait = WebDriverWait(self.webdriver, 10)
        likes = None
        element = wait.until(EC.presence_of_element_located((By.ID, "photos_snowlift")))
        dropdownButton = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fbPhotoSnowliftDropdownButton")))
        dropdownButton.click()
        divDownloadNotHidden = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.uiContextualLayerPositioner:not(.hidden_elem)")))
        waitDownload = WebDriverWait(divDownloadNotHidden, 10)
        imageUrlsDownload = waitDownload.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-action-type='download_photo']")))
        if imageUrlsDownload.__len__() == 0:
            url = ''
        else:
            url = imageUrlsDownload[0].get_attribute('href')
            imageUrlsDownload[0].click()
        likes = '0'
        feedbackElement = wait.until(EC.presence_of_element_located((By.ID, 'fbPhotoSnowliftFeedback')))
        try:
            likes = feedbackElement.find_element_by_class_name("_4arz").text
        except:
            pass
        dropdownButton.click()
        return [url, likes]

    def __get_DataImageTheater__(self):
        try:
            [url, likes] = self.function_for_DataImageTheater()
        except StaleElementReferenceException as e:
            print(e)
            time.sleep(1)
            [url, likes] = self.function_for_DataImageTheater()
        return [url, likes]

    def function_for_faster_DataImageTheater(self):
        wait = WebDriverWait(self.webdriver, 10)
        likes = None
        element = wait.until(EC.presence_of_element_located((By.ID, "photos_snowlift")))
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "stageWrapper")))
        imageUrlsDownload = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img[class='spotlight']")))
        if imageUrlsDownload.__len__() == 0:
            url = ''
        else:
            url = imageUrlsDownload[0].get_attribute('src')
            nameImage = self._get_name_in_string(url)
            processImage.getImageFromURL(url, nameImage)
        likes = '0'
        feedbackElement = wait.until(EC.presence_of_element_located((By.ID, 'fbPhotoSnowliftFeedback')))
        try:
            likes = feedbackElement.find_element_by_class_name("_4arz").text
        except:
            pass
        return [[url], likes]

    def __get_faster_DataImageTheater__(self):
        try:
            [url, likes] = self.function_for_faster_DataImageTheater()
        except StaleElementReferenceException as e:
            print(e)
            time.sleep(2)
            [url, likes] = self.function_for_faster_DataImageTheater()
        return [url, likes]

    def escapeTheater(self):
        self.press_key_in_page_html(Keys.ESCAPE)
        # Check Complete escape
        findEscape = self.webdriver.find_elements_by_class_name("_xlt")
        findEscape1 = self.webdriver.find_elements_by_class_name("layerCancel")
        if findEscape.__len__() > 0 or findEscape1.__len__() > 0:
            self.press_key_in_page_html(Keys.ESCAPE)

    def nextImageTheater(self):
        self.press_key_in_page_html(Keys.ARROW_RIGHT)
        time.sleep(1) # wait load page

    def getDataContainer(self, name: object, type_script: object) -> object:
        try:
            BrowseResultsContainer = self.webdriver.find_element_by_id(name)
        except NoSuchElementException:
            return 0
        childsUserContentWrapper = BrowseResultsContainer.find_elements_by_class_name('userContentWrapper')
        for childUserContentWrapper in childsUserContentWrapper:
            print('<-------------------->')
            contentpost = ""
            try:
                contentpost = childUserContentWrapper.find_element_by_class_name('userContent').text
            except NoSuchElementException as e:
                contentpost = 'Empty Content'
            # Get Image URL
            listImageURL = childUserContentWrapper.find_elements_by_css_selector(
                "a[rel='theater'][data-render-location='homepage_stream']")
            if listImageURL.__len__() == 0:
                print('Khong co Image')
                continue

            if listImageURL.__len__() == 1:
                url = []
                likes = None
                likes = self.getLikeShareinPost(childUserContentWrapper)
                self._clickFirstImageTheater_(listImageURL[0])
                try:
                    if type_script == 1:
                        [url, likes] = self.__get_faster_DataImageTheater__()
                    else:
                        [url, likes] = self.__get_DataImageTheater__()
                except TimeoutException as e:
                    [url, likes] = self.getDifferentDataImage()
                # update likes
                print(url)
                self.tinydbInfoAcc.insert(contentpost, likes, url)

            if listImageURL.__len__() > 1:
                likes = self.getLikeShareinPost(childUserContentWrapper)
                self._clickFirstImageTheater_(listImageURL[0])
                try:
                    [url, like] = self.getMultipleDataImageTheater(type_script)
                except TimeoutException as e:
                    [url, like] = self.getDifferentDataImage()
                self.getLikeShareinPost(childUserContentWrapper)
                print(url)
                self.tinydbInfoAcc.insert(contentpost, likes, url)
            self.escapeTheater()

    def add_cookie(self):
        pass

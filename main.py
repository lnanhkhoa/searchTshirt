#!/usr/bin/python
import os, time
import apps
cur_path = os.path.dirname(__file__)

from selenium.webdriver.common.keys import Keys

# Process Image
pathImage = 'img'
processImage = apps.ProcessImage(os.path.join(cur_path, pathImage))

# Information Users Facebook
user = "41201696@hcmut.edu.vn"
password = "lnak121104"
accountFacebook = apps.AccountsFacebook(user, password)

textSearch = 'i want this shirt'
functionsWebDriver = apps.FunctionsWebDriver('firefox')
functionsWebDriver.getURL('https://www.facebook.com/')
functionsWebDriver.login(accountFacebook)
searchPage = functionsWebDriver.getURL('https://www.facebook.com/search/str/' +textSearch +'/stories-keyword/today/date/stories/intersect')
functionsWebDriver.loadAllPostSearch()
print('load All Done')
# functionsWebDriver.clickSeeMore()
# functionsWebDriver.quit()

def main():
    driver = functionsWebDriver.getWebDriver()
    # driver.get("file:///C:/Users/khoa/PycharmProjects/seleniumPython/BrowserResults.html")
    BrowseResultsContainer = driver.find_element_by_id('BrowseResultsContainer')
    # childs = BrowseResultsContainer.find_elements_by_tag_name('img')
    childs = BrowseResultsContainer.find_elements('rel', 'theater')
    # for child in childs:
    #     if(child.size.get('width')>450):
    #         getImage (child.get_attribute('src'), child.id + '.jpg')


def getBrowseResultsBelowFold():
    driver = functionsWebDriver.getWebDriver()
    BrowseResultsBelowFold = driver.find_element_by_id('u_ps_0_3_0_browse_result_below_fold')
    


if __name__ == '__main__':
    print("==========================================")
    listName = functionsWebDriver.getNameContainer()
    for name in listName:
        print('')
        print('!!!===!!!' + name +'!!!===!!!')
        print('')
        functionsWebDriver.getDataContainer(name)
    pass

#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from time import sleep
import requests
import os

cur_path = os.path.dirname(__file__)
pathImg = 'img'

# user=input('Enter Email Id:')
user = "41201696@hcmut.edu.vn"
# pass=input('Enter Password:')
password = "lnak121104"
# capabilities = DesiredCapabilities.FIREFOX.copy()
# capabilities['marionette'] = False
# driver = webdriver.Firefox(capabilities=capabilities)
driver = webdriver.Firefox()
driver.get('https://www.facebook.com/')


# assert "facebook" in driver.title

def login():
    print("Opened facebook")
    username_box = driver.find_element_by_id('email')
    username_box.send_keys(user)
    print("Email Id entered")
    sleep(1)

    password_box = driver.find_element_by_id('pass')
    password_box.send_keys(password)
    print("Password entered")

    login_box = driver.find_element_by_id('loginbutton')
    login_box.click()

    print("Done")

def main():
    # driver.get("file:///C:/Users/khoa/PycharmProjects/seleniumPython/BrowserResults.html")
    BrowseResultsContainer = driver.find_element_by_id('BrowseResultsContainer')
    childs = BrowseResultsContainer.find_elements_by_tag_name('img')
    for child in childs:
        if(child.size.get('width')>450):
            getImage (child.get_attribute('src'), child.id + '.jpg')

def getImage(pic_url, name):
    file = os.path.join(cur_path, pathImg, name)
    with open(file, 'wb') as handle:
        response = requests.get(pic_url, stream=True)
        if not response.ok:
            print (response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)



def getBrowseResultsBelowFold():
    BrowseResultsBelowFold = driver.find_element_by_id('u_ps_0_3_0_browse_result_below_fold')
    


if __name__ == '__main__':
    login()
    driver.get(
        'https://www.facebook.com/search/str/i%20want%20this%20shirt/stories-keyword/today/date/stories/intersect')
    main()
    driver.quit()

#!/usr/bin/python
import os, time
import apps
import logging
from config import DATABASE_CONFIG
from apps import FunctionsWebDriver

cur_path = os.path.dirname(__file__)
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler(os.path.join(cur_path, 'log/myapp.log'))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

tinydbInfoAcc = apps.TinyDBInfoAcc()
functionsWebDriver = apps.FunctionsWebDriver('firefox', tinydbInfoAcc)

# Information Users Facebook
user = DATABASE_CONFIG['username']
password = DATABASE_CONFIG['password']
accountFacebook = apps.AccountsFacebook(user, password)

# Scripts
textSearch = DATABASE_CONFIG['textsearch']
type_of_run_script = DATABASE_CONFIG['type_of_run_script']

def preprocess():
    functionsWebDriver.getURL('https://www.facebook.com/')
    functionsWebDriver.login(accountFacebook)
    searchPage = functionsWebDriver.getURL(
        'https://www.facebook.com/search/str/' + textSearch + '/stories-keyword/today/date/stories/intersect')
    functionsWebDriver.loadAllPostSearch()
    print('load All Done')
    # functionsWebDriver.clickSeeMore()

def databasesShow():
    tinydbInfoAcc.showAll()


def main():
    print("==========================================")
    listName = functionsWebDriver.getNameContainer()
    len1ist = len(listName)
    for name in listName:
        print('')
        print('!!!===!!!' + name + '!!!===!!!')
        print('')
        functionsWebDriver.getDataContainer(name, type_of_run_script)
    # functionsWebDriver.getDataContainer('fbBrowseScrollingPagerContainer0', type_of_run_script)


def test():
    pass

if __name__ == '__main__':
    start = time.time()
    preprocess()
    main()
    functionsWebDriver.quit()
    end = time.time()
    print("Script xai het :" + str(end - start))

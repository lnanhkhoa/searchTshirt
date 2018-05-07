#!/usr/bin/python
import os, time
import apps
import logging

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
user = "voagki27393@piapia.gq"
password = "qeqeqe123"
accountFacebook = apps.AccountsFacebook(user, password)

textSearch = 'i want this shirt'


def preprocess():
    functionsWebDriver.getURL('https://www.facebook.com/')
    functionsWebDriver.login(accountFacebook)
    searchPage = functionsWebDriver.getURL(
        'https://www.facebook.com/search/str/' + textSearch + '/stories-keyword/today/date/stories/intersect')
    functionsWebDriver.loadAllPostSearch()
    print('load All Done')


# functionsWebDriver.clickSeeMore()
# functionsWebDriver.quit()

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
        functionsWebDriver.getDataContainer(name)
    # functionsWebDriver.getDataContainer(listName[0])


def test():
    pass

if __name__ == '__main__':
    start = time.time()
    preprocess()
    main()
    end = time.time()
    print("Script xai het :" + str(end - start))

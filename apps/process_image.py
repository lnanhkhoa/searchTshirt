
import os, time, requests

class ProcessImage():

    def __init__(self, storedImagePath):
        self.storedImagePath = storedImagePath

    def getImageFromURL(self, pic_url, name):
        file = os.path.join(self.storedImagePath, name)
        with open(file, 'wb') as handle:
            response = requests.get(pic_url, stream=True)
            if not response.ok:
                print (response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)



from tinydb import TinyDB, Query


class TinyDBInfoAcc:
    def __init__(self):
        self.db = TinyDB('db.json')
        self.User = Query()

    def insert(self, content_post: object, like_share: object, urls: object = None) -> object:
        if urls is None:
            urls = []
        self.db.insert({
            'urls': urls,
            'like_share': like_share,
            'content_post': content_post
        })

    def showAll(self):
        for item in self.db:
            print(item)

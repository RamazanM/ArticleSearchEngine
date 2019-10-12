import pymongo

class ArticleDatabase(object):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["ArticleSearch"]
    def insertJournals(self,journals):
        self.db.journals.insert_many(journals)

    def hasJournal  (self,journal):
        return self.db.journals.count_documents(journal,limit=1)>0
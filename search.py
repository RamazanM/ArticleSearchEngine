from lxml import html
import requests
import database.ArticleDatabase

all_journals="https://dergipark.org.tr/tr/pub/explore/journals"
db=database.ArticleDatabase()

page_index=1
at_the_end=True

while not at_the_end:
    next_page_btn_selector="/html/body/div/div/div/div/div/div/div/div/div[2]/div/div/div[3]/div/div/a[2]"
    
    journalsPage = html.fromstring(requests.get(all_journals+"/"+str(page_index)).text)
    journalsXml=journalsPage.xpath("/html/body/div/div/div/div/div/div/div/div/div[2]/div/div/div[2]/table/tbody/tr/td")
    at_the_end = journalsPage.xpath(next_page_btn_selector)[0].attrib.get("href")=="javascript: ;"
    journalList=[]
    for j in journalsXml:
        #name
        name=j.find("h5/a").text
        #url
        url=j.find("h5/a").attrib.get("href")
        #publisher
        publisher=j.find("h6").text
        categoriesXml=j.find("div")
        #categories
        categories=[]
        for c in categoriesXml:
            categories.append(c.text)
        journal={"name":name,"url":url,"publisher":publisher,"categories":categories}
        if not db.hasJournal(journal):
            journalList.append(journal)
    page_index+=1
    if len(journalList)>0:
        db.insertJournals(journalList)
    

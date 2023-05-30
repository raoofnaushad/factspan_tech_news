

from src.utils import *
from src.config import *
from scrapers import toi, oai

import random

class Scraper():
    def __init__(self, contents):
        self.contents = contents
        
    def scrape_news(self, site):
        scraped = list()
        
        try:
            if site == "TOI":
                scraped = toi.main()

            if site == "OPENAI":
                scraped = oai.main()

            print(f"Scraped contents from {site} is: {len(scraped)}")
            return scraped

        except Exception as ex:
            print(f"Problem with Scraping: {str(ex)}")
            return scraped
    
    def write_news_to_db(self):
        try:
            if not self.contents:
                print(f'No data scraped. Thus nothing to write')
                exit()

            random.shuffle(self.contents)
            
            db = connect_mong()
            coll = db.news
            coll.delete_many({"date" : today})
            print(f"Data deleted from mongo for the date: {today}")
            coll.insert_many(self.contents)
            print(f"{len(self.contents)} number of data inserted to mongo for the date: {today}")
            
        except Exception as ex:
            print(f"Problem with writing to db: {str(ex)}")



def start_scraping():
    contents = list()    
    scrape = Scraper(contents)
    
    ## Scraping 
    scrape.contents.extend(scrape.scrape_news("TOI"))
    scrape.contents.extend(scrape.scrape_news("OPENAI"))

    # Writing to DB
    scrape.write_news_to_db()
    

if __name__ == "__main__":
    start_scraping()
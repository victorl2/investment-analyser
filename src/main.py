from dotenv import load_dotenv
from services.scrapper import Scrapper
import os
    
if __name__ == '__main__':
    load_dotenv('../.env')

    url_sources = os.getenv('sources').replace('\n', '').split(',')
    url_sources = [url.strip() for url in url_sources]
    scrapper = Scrapper(url_sources)

    for url in url_sources:
        print(f"fetching articles from {url}")
        articles = scrapper.fetch_articles(url)
        scrapper.save_articles(articles)
        print(f"found {len(articles)} articles")
        print("##########\n")
    
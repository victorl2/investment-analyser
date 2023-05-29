import requests
from bs4 import BeautifulSoup
import datetime
import os

class Scrapper:
    def __init__(self, url_sources, files_path="data"):
        self.url_sources = url_sources
        self.files_path = files_path

    def __fetch_data(self, url) -> str:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None

    def __parse_html(self, html) -> list:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a')

        parsed_links = []
        for link in links:
            href = link.get('href')
            title = link.get('title')
            content = link.string
            parsed_links.append((href, title, content))
        return parsed_links

    def fetch_articles(self, url) -> list:
        html = self.__fetch_data(url)
        if html is None:
            return []   
    
        output = [] 
        hashmap = {}
    
        for link in self.__parse_html(html):
            if link[0] is None or url not in link[0] or link[0] in hashmap:
                continue
            title = link[1] if link[1] is not None else link[2]
            split_link = link[0].split('-')
    
            if len(split_link) < 5:
                continue
            if title is None:
                prefix = split_link[0].split("/")
                sufix = " ".join(split_link[1:])
                title = prefix[len(prefix)-1] + " " + sufix
                title = title.replace("/", "").strip()
            hashmap[link[0]] = True
            output.append((link[0], title))
        return output

    def save_articles(self, articles:list) -> None:
        # save articles to a file
        if articles is None or len(articles) == 0:
            return
        
        url = articles[0][0].split('/')[2].replace('www.', '')
        source_name = url.split('.com')[0].replace('.','').replace('-', '').strip()
        current_date = datetime.datetime.now().strftime("%d-%m-%Y")

        # create folder if not exists
        if not os.path.exists(self.files_path):
            os.makedirs(self.files_path)

        with open(f"{self.files_path}/articles__{current_date}__{source_name}.csv", "w") as f:
            f.write("url,title\n")
            for article in articles:
                f.write(f"{article[0]},{article[1]}\n")
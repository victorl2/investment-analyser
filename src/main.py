import requests
import datetime
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')

    parsed_links = []
    for link in links:
        href = link.get('href')
        title = link.get('title')
        content = link.string
        parsed_links.append((href, title, content))
    return parsed_links

def fetch_articles(url, file_path="../data"):
    source_name = url.split('//')[1].split('.')[1]
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")

    # if exists file dont do anything
    if os.path.exists(f'{source_name}-articles-{current_date}.csv'):
        print("file already exists")
        return

    html = fetch_data(url)
    if html is None:
        return

    hasmap = {}
    source_name = url.split('//')[1].split('.')[1]
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")
    
    with open(f'{file_path}/{source_name}-links-{current_date}.csv', 'w') as f:
        f.write('link,title\n')
        for link in parse_html(html):
            if link[0] is None or url not in link[0] or link[0] in hasmap:
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

            hasmap[link[0]] = True
            f.write(f'{link[0]},{title}\n')
    
if __name__ == '__main__':
    load_dotenv('../.env')
    url_sources = os.getenv('sources').replace('\n', '').strip().split(',')
    for url in url_sources:
        print(f"fetching articles from {url}")
        fetch_articles(url)
    
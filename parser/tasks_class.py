from bs4 import BeautifulSoup
from celery import Celery, Task
import requests
import xmltodict

CELERY_BROKER = 'redis://localhost'
SEARCH_PAGE1 = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=1'
SEARCH_PAGE2 = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=2'

app = Celery('main', broker=CELERY_BROKER)

class Page_parser(Task):
    def run(self, page_url):
        response = requests.get(page_url, headers={'User-Agent': 'Custom'})
        soup = BeautifulSoup(response.content, features='html.parser')
        docs = soup.find_all(class_='registry-entry__header-top')
        xml_links = []
        for doc in docs:
            link = doc.find(attrs={"target": "_blank"})
            href = link['href'].replace('view.html', 'viewXml.html')
            xml_links.append(f'https://zakupki.gov.ru/{href}')
        for xml_link in xml_links:
            Link_parser.delay(xml_link)

class Link_parser(Task):
    def run(self, link):
        response = requests.get(link, headers={'User-Agent': 'Custom'}) 
        data = xmltodict.parse(response.content)
        res = None
        for key, val in data.items():
            if 'ns7:epNotification' in key:
                res = val 
        if res:
            pretty_content = f"Link:{link} -> Date:{res.get('commonInfo')['publishDTInEIS']}"
            print(pretty_content)

Page_parser = app.register_task(Page_parser())
Link_parser = app.register_task(Link_parser())

Page_parser.delay(SEARCH_PAGE1)
Page_parser.delay(SEARCH_PAGE2)

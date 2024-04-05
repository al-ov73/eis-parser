from bs4 import BeautifulSoup
from celery import Celery
import requests
import xmltodict

app = Celery('main', broker='redis://localhost')

search_page1 = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=1'
search_page2 = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=2'

@app.task
def parse_page(page_url):
    response = requests.get(page_url, headers={'User-Agent': 'Custom'})
    soup = BeautifulSoup(response.content, features='html.parser')
    docs = soup.find_all(class_='registry-entry__header-top')
    xml_links = []
    for doc in docs:
        link = doc.find(attrs={"target": "_blank"})
        href = link['href'].replace('view.html', 'viewXml.html')
        xml_links.append(f'https://zakupki.gov.ru/{href}')
    for xml_link in xml_links:
        parse_link.delay(xml_link)

@app.task
def parse_link(link):
    response = requests.get(link, headers={'User-Agent': 'Custom'}) 
    data = xmltodict.parse(response.content)
    res = None
    for key, val in data.items():
        if 'ns7:epNotification' in key:
            res = val 
    if res:
        pretty_content = f"Link:{link} -> Date:{res.get('commonInfo')['publishDTInEIS']}"
        print(pretty_content)

parse_page.delay(search_page1)
parse_page.delay(search_page2)

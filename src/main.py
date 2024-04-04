from bs4 import BeautifulSoup
import requests

search_page1 = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=1'
search_page2 = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=2'

def response_from(url):
    response = requests.get(url)
    response.raise_for_status()
    return response

def get_tags(url):
    html_content = response_from(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    print(soup);
    # if soup.h1:
    #     h1 = str(soup.h1.string)
    # else:
    #     h1 = ''
    # if soup.title:
    #     title = str(soup.title.string) if soup.title.string else ''
    # else:
    #     title = ''
    # if soup.find('meta', {'name': 'description'}):
    #     description = soup.find('meta', {'name': 'description'}).get('content')
    # else:
    #     description = ''
    # return h1, title, description
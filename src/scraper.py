import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
from src.consts import *


def scrape(url: str = None):
    if not url:
        return

    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    data = {}
    data['name'] = scrape_name(soup)
    data['price'] = scrape_price(soup)
    data['location'] = scrape_location(soup)
    data['mileage'] = scrape_mileage(soup)
    data['params'] = scrape_params(soup)
    data['description'] = scrape_description(soup)
    data['phones'] = scrape_phones(soup)

    data = {k: v for k, v in data.items() if v is not None}

    return data


def scrape_name(soup):
    return soup.find('h1', class_='head').text.strip()


def scrape_price(soup):
    div = soup.find('div', class_='price_value')
    strong = div.find('strong')
    return strong.text.strip()


def scrape_location(soup):
    section = soup.find('section', id='userInfoBlock')
    divs = section.find_all('div', class_='item_inner')
    div = [div for div in divs if not div.find('strong')][0]
    return div.text.strip()


def scrape_mileage(soup):
    div = soup.find('div', class_='base-information')
    span = div.find('span', 'size18')
    return span.text.strip()


def scrape_params(soup):
    details = soup.find('div', id='details')
    divs = details.find_all('dd', class_='')
    params = {}
    for div in divs:
        label = div.find('span', class_='label')
        if not label or label.text not in TECH_INFO_TABLE:
            continue
        argument = div.find('span', class_='argument')
        params[TECH_INFO_TABLE[label.text]] = argument.text

    return params


def scrape_description(soup):
    div = soup.find('div', class_='full-description')
    if div:
        return div.get_text('\n').strip()
    return None


def scrape_phones(soup):
    phones = []

    scripts = soup.select('script[class^="js-user-secure-"]')
    hash = scripts[0].get('data-hash')
    id = soup.find('body').get('data-auto-id')
    url = "https://auto.ria.com/users/phones/"+id+"?hash="+hash
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = json.loads(requests.get(url, headers=headers).text)

    for phone in response['phones']:
        phoneNumber = phone['phoneFormatted'].replace(' ', '')
        phoneNumber = phoneNumber.replace('(', '')
        phoneNumber = phoneNumber.replace(')', '')
        phones.append(phoneNumber)
    return phones


def main():
    url = "https://auto.ria.com/uk/auto_land_rover_freelander_34752113.html"
    pprint(scrape(url))


if __name__ == '__main__':
    main()

import requests
from bs4 import BeautifulSoup
import json

TECH_INFO_TABLE = {
    'Двигун': 'engine',
    'Привід': 'drive',
    'Коробка передач': 'transmission'
}


def parse(url: str = None):
    if not url:
        return

    # Send an HTTP request to the specified URL and fetch the HTML content
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    data = {}
    data['name'] = parse_name(soup)
    data['price'] = parse_price(soup)
    data['location'] = parse_location(soup)
    data['mileage'] = parse_mileage(soup)
    data['params'] = parse_params(soup)
    data['description'] = parse_description(soup)
    data['phones'] = parse_phones(soup)

    data = {k: v for k, v in data.items() if v is not None}

    # print(data)
    return data


def parse_x(soup):
    pass


def parse_name(soup):
    return soup.find('h1', class_='head').text.strip()


def parse_price(soup):
    div = soup.find('div', class_='price_value')
    strong = div.find('strong')
    return strong.text.strip()


def parse_location(soup):
    section = soup.find('section', id='userInfoBlock')
    div = section.find('div', class_='item_inner')
    return div.text.strip()


def parse_mileage(soup):
    div = soup.find('div', class_='base-information')
    span = div.find('span', 'size18')
    return span.text.strip()


def parse_params(soup):
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


def parse_description(soup):
    div = soup.find('div', class_='full-description')
    if div:
        return div.decode_contents()
    return None


def parse_phones(soup):
    hash = soup.select('script[class^="js-user-secure-"]')[0].get('data-hash')
    id = soup.find('body').get('data-auto-id')
    url = "https://auto.ria.com/users/phones/"+id+"?hash="+hash
    response = json.loads(requests.get(url).text)
    phones = []
    for phone in response['phones']:
        phoneNumber = phone['phoneFormatted'].replace(' ', '')
        phoneNumber = phoneNumber.replace('(', '')
        phoneNumber = phoneNumber.replace(')', '')
        phones.append(phoneNumber)
    return phones


def main():
    url = "https://auto.ria.com/uk/auto_mercedes_benz_vito_36114523.html"
    parse(url)


if __name__ == '__main__':
    main()

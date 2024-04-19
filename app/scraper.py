import requests
from bs4 import BeautifulSoup

def scrape_stars_list():
    url = 'https://iau.org/public/themes/naming_stars/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    stars_list = []
    for row in soup.select('.ent-name'):
        stars_list.append(row.text.strip())
    return stars_list

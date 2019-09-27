import logging
import requests
from bs4 import BeautifulSoup
from itertools import islice
import json

logger = logging.getLogger(__name__)

def get_kids_projects():
    page = requests.get('https://www.thebudgetdiet.com/45-diy-fun-summer-projects-to-do-with-your-kids')
    soup = BeautifulSoup(page.content, 'lxml')

    content = soup.find('div', class_='entry-content').find_all(['h2','p'])

    projects = []
    icontent = iter(content)
    for child in icontent:
        if child.name == 'h2':
            title = child.text.strip('0123456789. ').replace('\xa0','')
            next_item = next(icontent)
            while next_item.find('a') is None:
                next_item = next(icontent)
                link = next_item.find('a')['href']
            projects.append({'title':title, 'link':link})

    with open('./data/random_projects.json', 'w', newline='') as json_file:
        json.dump(projects, json_file)

if __name__ == '__main__':
    get_kids_projects()

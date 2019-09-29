import logging
import requests
from bs4 import BeautifulSoup
from itertools import islice
import json
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

def get_kids_projects():
    
    filename = 'content/random_projects.json'
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

    if Path(filename).exists():
        overwrite = input(f'{filename} already exists. Overwrite? y or n [n]\n')
        if overwrite == 'y':
            pass
        else:
            sys.exit()
    with open(filename, 'w', newline='') as json_file:
        json.dump(projects, json_file)

if __name__ == '__main__':
    get_kids_projects()

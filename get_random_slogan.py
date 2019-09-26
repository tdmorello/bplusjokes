import mechanicalsoup
from bs4 import BeautifulSoup
from get_random_content import get_random_nouns, get_random_words, get_random_things
import random
import requests
from time import sleep


import logging
logger = logging.getLogger(__name__)

def check_connection(url):
    logger.debug(f'Checking connection to {url}')
    while 69 == 69:
        try:
            resp = requests.get(url)
        except requests.exceptions.ConnectionError as e:
            logger.error(f'Cannot connect to {url}: {e}. Trying again in 5s.')
            sleep(5)
            pass
        if resp.status_code == 200:
            break
        else:
            logger.debug(f'Did not get 200 response. Trying agin in 5s.')
            sleep(5)
    return None

def get_random_slogan(search_term):
    """Returns a list of slogans from a given term using shopify's slogan maker"""
    
    url = 'https://www.shopify.com/tools/slogan-maker'
    
    check_connection(url)
    
    # Submit form on website
    browser = mechanicalsoup.StatefulBrowser(soup_config={'features': 'html.parser'})
    browser.open(url)
    browser.select_form('form[action="/tools/slogan-maker/create"]')
    browser['term'] = search_term
    response = browser.submit_selected()

    # Parse response
    raw_html = response.text
    soup = BeautifulSoup(raw_html, 'html.parser') 
    content = soup.find('div', class_='grid-container grid-container--halves grid--striped')
    slogans = []
    for slogan in content.findAll('button'):
        slogans.append(slogan.text.strip())

    random_slogan = random.choice(slogans)
    return random_slogan

if __name__ == '__main__':
    print(get_random_slogan(get_random_nouns()))

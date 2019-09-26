import mechanicalsoup
from bs4 import BeautifulSoup
from get_random_content import get_random_noun, get_random_word, get_random_thing
import random
import requests
from time import sleep
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s')
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

def double_seq(start):
    curr = start
    while True:
        yield curr
        curr = curr * 2

def get_random_slogans(num):
    """Returns a list of slogans from random nouns"""
    
    url = 'https://www.shopify.com/tools/slogan-maker'
    
    check_connection(url)
    
    # Connect once to webpage
    browser = mechanicalsoup.StatefulBrowser(soup_config={'features': 'html.parser'})
    browser.open(url)
    
    slogans = []
    
    for _ in range(num):
        random_word = get_random_noun()
        
        # Submit form on website
        browser.select_form('form[action="/tools/slogan-maker/create"]')
        browser['term'] = random_word
        response = browser.submit_selected()
        # # Wait to avoid HTTP 429 response
        sleep(1)
        
        print(response.status_code)
        if response.status_code == 429:
            iterator_ = double_seq(10)
            while response.status_code == 429:
                sleep_time = next(iterator_)
                logger.debug(f'Got 429 response, sleeping for {sleep_time}s')
                # this would be the perfect place for an iterator that increases wait time
                # by 1.5 each round
                for s in range(sleep_time):
                    print("."*s, end='\r')
                    sleep(1)
                # retry
                # Submit form on website
                logger.debug('Trying again')
                # Connect once to webpage
                browser = mechanicalsoup.StatefulBrowser(soup_config={'features': 'html.parser'})
                browser.open(url)
                browser.select_form('form[action="/tools/slogan-maker/create"]')
                browser['term'] = random_word
                response = browser.submit_selected()
                print(response.status_code)
                # Wait to avoid HTTP 429 response
        
        # Parse response
        raw_html = response.text
        soup = BeautifulSoup(raw_html, 'html.parser') 
        content = soup.find('div', class_='grid-container grid-container--halves grid--striped')
        for slogan in random.choice(content.findAll('button')):
            print(slogan.strip())
            slogans.append(slogan.strip())
    
    # return slogans
    return slogans

if __name__ == '__main__':
    print(get_random_slogans(10))

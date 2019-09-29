from bs4 import BeautifulSoup
import json
import logging
import mechanicalsoup
import random
import requests
from time import sleep


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s : %(levelname)s : %(message)s')
logger = logging.getLogger(__name__)


def check_connection(url):
    logger.debug(f'Checking connection to {url}')
    
    while 69 == 69:
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError as e:
            logger.error(f'Cannot connect to {url}: {e}. Trying again in 5s.')
            sleep(5)
            pass
        if response.status_code == 200:
            break
        else:
            logger.debug(f'Did not get 200 response. Trying agin in 5s.')
            sleep(5)
    return response


def double_seq(start):
    """Generator to produce sequence of doubled numbers"""
    curr = start
    while True:
        yield curr
        curr = curr * 2


def get_random_content(content_file):
    """Options are nouns, things, and words"""
    def get_random_items():
        with open(f'content/{content_file}') as jsonfile:
            return json.load(jsonfile)
    def get_random_item():
        return random.choice(get_random_items())
    return get_random_items, get_random_item

###
get_words, get_word = get_random_content('random_words.json')
get_things, get_thing = get_random_content('random_things.json')
get_nouns, get_noun = get_random_content('random_nouns.json')
get_projects, get_project = get_random_content('random_projects.json')


def get_slogan():
    """Returns a single slogan from shopify's slogan maker"""

    url = 'https://www.shopify.com/tools/slogan-maker'

    search_term = get_noun()
    check_connection(url)

    # Submit form on website
    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'html.parser'})
    browser.open(url)
    browser.select_form('form[action="/tools/slogan-maker/create"]')
    browser['term'] = search_term
    response = browser.submit_selected()

    # Parse response
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find(
        'div', class_='grid-container grid-container--halves grid--striped')

    slogan_list = [slogan.text.strip() for slogan in content.findAll('button')]

    slogan = random.choice(slogan_list)
    return slogan

def get_slogans(n):
    """More efficient for generating a list of slogans because it only connects
    to the webpage one time. Also, it handles 429 responses."""

    url = 'https://www.shopify.com/tools/slogan-maker'
    check_connection(url)
    
    # Connect to website
    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'html.parser'})
    response = browser.open(url)

    slogans = []
    for _ in range(n):
        # Get a list of slogans from a random word then choose one slogan from the list
        search_term = get_noun()
        
        doubled = double_seq(15)

        # Fill in and submit the form
        browser.select_form('form[action="/tools/slogan-maker/create"]')
        browser['term'] = search_term
        response = browser.submit_selected()

        while response.status_code == 429:
            # Sleep to avoid another 429
            sleep_time = next(doubled)
            logger.debug(f'Got 429 response, sleeping for {sleep_time}s')
            sleep(sleep_time)

            # Reconnect to webpage
            logger.debug('Trying to connect again')
            response = browser.open(url)
            
            # Resubmit form
            browser.select_form(
                'form[action="/tools/slogan-maker/create"]')
            browser['term'] = search_term
            response = browser.submit_selected()
    
        # Parse response
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find(
            'div', class_='grid-container grid-container--halves grid--striped')
        slogan = random.choice(content.findAll('button'))
        print(slogan.text.strip())
        slogans.append(slogan.text.strip())
        
        # Sleep to prevent 429
        sleep(1)
        
    return slogans

def get_topic():
    url = 'https://www.conversationstarters.com/random.php'
    response = check_connection(url)
    
    while response.status_code != 200:
        response = requests.get(url)
        status_code = response.status_code
        sleep(5)

    soup = BeautifulSoup(response.text, features="lxml")
    return soup.text

def main():
    print(get_slogans(5))

if __name__ == '__main__':
    main()

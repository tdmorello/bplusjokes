# https://www.conversationstarters.com/generator.php

import requests
from bs4 import BeautifulSoup
from time import sleep

def get_random_topic():
    status_code = 0
    while status_code != 200:
        resp = requests.get('https://www.conversationstarters.com/random.php')
        status_code = resp.status_code
        sleep(2)

    soup = BeautifulSoup(resp.text, features="lxml")
    return soup.getText()


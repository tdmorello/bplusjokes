import mechanicalsoup
from bs4 import BeautifulSoup

def get_random_slogan(search_term):
    """Returns a list of slogans from a given term using shopify's slogan maker"""
    
    # Submit form on website
    browser = mechanicalsoup.StatefulBrowser()
    browser.open('https://www.shopify.com/tools/slogan-maker')
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
    
    return slogans
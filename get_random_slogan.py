import mechanicalsoup
from bs4 import BeautifulSoup

search_term = 'kitty'

browser = mechanicalsoup.StatefulBrowser()

browser.open('https://www.shopify.com/tools/slogan-maker')

browser.select_form('form[action="/tools/slogan-maker/create"]')

browser['term'] = search_term

response = browser.submit_selected()

raw_html = response.text

soup = BeautifulSoup(raw_html, 'html.parser') 

content = soup.find('div', class_='content')

slogans = []
for slogan in content.findAll('button'):
    slogans.append(slogan.text.strip())

print(len(slogan))
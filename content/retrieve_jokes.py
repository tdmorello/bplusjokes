from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import csv
import datetime
import sys
from pathlib import Path


def main():
    jokes_filename = 'dog_jokes.csv'
    target_url = "https://www.care.com/c/stories/7403/the-40-funniest-dog-jokes-for-kids-of-all-age/"
    
    page = get(target_url)
    soup = BeautifulSoup(page.content, 'html.parser') 
    content = soup.find('div', class_='content')  
    
    jokes = []
    joke = []

    # Date first joke should be sent out
    start_date = datetime.date(2019, 9, 25)
    
    count = 0
    jokes.append(['send_date','setup','punchline'])
    for ptag in content.findAll('p')[1:]: # the first tag is not part of a joke
        if (ptag.text[0] == 'Q'):
            joke_date = start_date + datetime.timedelta(count)
            count += 1
            question = ptag.text[3:]
            joke.append(joke_date)
            joke.append(question)
        if (ptag.text[0] == 'A'):
            answer = ptag.text[3:]
            joke.append(answer)
            jokes.append(joke)
            joke = []
    
    if Path(jokes_filename).exists():
        overwrite = input(f'{jokes_filename} already exists. Overwrite? y or n [n]\n')
        if overwrite == 'y':
            pass
        else:
            sys.exit()
    with open(jokes_filename, 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     for j in jokes:
        wr.writerow(j)


if __name__ == '__main__':
    main()

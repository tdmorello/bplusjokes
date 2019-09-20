from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import csv
import datetime


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def main():
    target_url = "https://www.care.com/c/stories/7403/the-40-funniest-dog-jokes-for-kids-of-all-age/"
    raw_html = simple_get(target_url)
    soup = BeautifulSoup(raw_html, 'html.parser') 
    content = soup.find('div', class_='content')  
    jokes = []
    joke = []

    # Date first joke should be sent out
    start_date = datetime.date(2019, 9, 15)
    
    count = 0
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
    with open('dog_jokes.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     for j in jokes:
        wr.writerow(j)


if __name__ == '__main__':
    main()

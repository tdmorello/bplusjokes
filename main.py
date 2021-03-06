import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import datetime
import logging
import sys
import argparse
from time import sleep
import json
import random

from get_content import get_slogan, get_slogans, get_topic, get_project

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s : %(levelname)s : %(message)s')
logger = logging.getLogger(__name__)

# TODO:
# - Add a check that every joke has a send-date

def get_csv_content(csv_file):
    """Create ordered dictionary from a csv file content"""
    logger.debug(f"Getting content from {csv_file}")
    try:
        with open(csv_file, encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            data = []
            for row in reader:
                data.append(row)
            logger.debug(f"Found {len(data)} entries in {csv_file}")
            return data
    except IOError as e:
        logger.error(msg=e)


def get_todays_joke(jokes):
    logger.debug("Finding today's joke.")
    for joke in jokes:
        entry_date = datetime.datetime.strptime(
            joke['send_date'], '%Y-%m-%d').date()
        if entry_date == datetime.date.today():
            logger.info(
                f"Today's joke is: {joke['setup']} {joke['punchline']}")
            return joke
    logger.error("No jokes for today were found.")
    sys.exit()


def main():
    # Get args
    parser = argparse.ArgumentParser()
    # With default choice
    parser.add_argument('-m', '--runmode', default='test', choices=['test', 'dry', 'real'],
                        help='mode to run the script (default is test run)')
    args = parser.parse_args()
    runmode = args.runmode
    logger.debug(f'This is a {runmode.upper()} run.')

    # Server connection info
    sender_email = "bplusjokes@gmail.com"
    sender_name = "B+ Jokes"
    password = "epcjxgyzlmijdyui"

    # Prepare joke
    jokes = get_csv_content("content/dog_jokes.csv")
    todays_joke = get_todays_joke(jokes)
    joke_setup = todays_joke['setup']
    joke_punchline = todays_joke['punchline']

    # Prepare contacts
    if runmode == 'test':
        contacts = get_csv_content("content/contacts_test.csv")
    else:
        contacts = get_csv_content("content/contacts.csv")

    # Prepare business slogans
    slogans = get_slogans(len(contacts))

    # Prepare projects
    projects = [get_project() for _ in range(len(contacts))]
    print(projects)

    # Prepare conversation starters
    topics = [get_topic() for _ in range(len(contacts))]

    # Send mail

    for i, contact in enumerate(contacts):
        slogan = slogans[i]
        recipient_name = contact['name']
        recipient_email = contact['email']

        if recipient_email == '':
            logger.error(
                f'Contact email for {recipient_name} cannot be blank. Skipping...')
            continue
        else:
            recipient_email = contact['email']

        logger.info(f"Sending email to {recipient_name} at {recipient_email}")

        # MESSAGE
        message = MIMEMultipart("alternative")
        message["Subject"] = f'J of the Day: {joke_setup}'
        message["From"] = sender_name + ' <' + sender_email + '>'
        message["To"] = recipient_email

        # Create the plain-text and HTML version of your message
        text = f"""\
    Yo {recipient_name}!
    Thank you for your irreversible subscription to Dog Joke of the Day.
    Here's your dog joke of the day!

    {todays_joke['setup']}
    {todays_joke['punchline']}

    Looking to start a new business? Consider this slogan!
    {slogan}
    
    Making friends can be hard! Here's a conversation starter to try today.
    {get_topic()}
    """

        html = f"""\
    <html>
      <body>
        <p>To whom it may concern:<br><br>
          Thank you for your everlasting subscription to Dog Joke of the Day.<br>
          Here's your dog joke of the day!
        </p>
        <br>
        
        <h1>#JokeSection</h1>
        <p>
          <strong>{todays_joke['setup']}</strong><br><br>
          <i>{todays_joke['punchline']}</i>
        </p>
        <br>
        
        <h1>#KidsSection</h1>
        <p>
          Bored? Here's a project to do this weekend!<br><br>
          <a href="{projects[i]['link']}">{projects[i]['title']}</a>
        </p>
        <br>
        
        <h1>#BusinessSection</h1>
        <p>
          Looking to start a new business? Consider this slogan!<br><br>
          <b>{slogan}</b>
        </p>
        <br><br>

        
        <h1>#SocialSection</h1>
        <p>
          Making friends can be hard! Here's a conversation starter to try today.<br><br>
          <b>{topics[i]}</b>
        </p>
        <br><br>
        
        
        <p>
        Already have a Dog Joke of the Day provider?
        <a href="http://endless.horse">Click here to unsubscribe</a>
        </p>
      </body>
    </html>
    """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        if runmode == 'dry':
            continue
        # Create secure connection with server and send email
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, recipient_email, message.as_string()
                )
            logger.debug(f'Email {i} to {recipient_name} was sent.')
        except smtplib.SMTPRecipientsRefused as e:
            logger.error(f'RecipientsRefused: {recipient_name}: {e}')

    return None


if __name__ == '__main__':
    main()

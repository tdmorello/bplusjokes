import smtplib, ssl
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

from get_random_slogan import get_random_slogan
from get_random_slogans import get_random_slogans
from get_random_topic import get_random_topic

logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(levelname)s : %(message)s')

logger = logging.getLogger(__name__)

# TODO:
# - Add a check that every joke has a send-date
# - Add logging verbosity to sys args


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
    logger.error(msg = e)

def find_todays_joke(jokes):
  logger.debug("Finding today's joke.")
  for joke in jokes:
    entry_date = datetime.datetime.strptime(joke['send_date'], '%Y-%m-%d').date()
    if entry_date == datetime.date.today():
      logger.debug("Found today's joke.")
      logger.info(f"Today's joke is: {joke['setup']} {joke['punchline']}")
      return joke
  logger.error("No jokes for today were found.")
  sys.exit()
  
def get_random_projects(count):
  with open('./data/random_projects.json', mode='r') as jsonfile:
    random_projects = json.load(jsonfile)
    projects = random.sample(random_projects,count)
    return projects

def main():
  # Get args
  parser = argparse.ArgumentParser()
  # With default choice
  parser.add_argument('-m', '--runmode', default='test', choices=['test','dry','real'],
                      help='mode to run the script (default is test run)')
  args = parser.parse_args()
  runmode = args.runmode
  logger.debug(f'This is a {runmode.upper()} run.')
  
  # Server connection info
  sender_email = "bplusjokes@gmail.com"
  sender_name = "B+ Jokes"
  password = "epcjxgyzlmijdyui"

  # Prepare joke
  jokes = get_csv_content("dog_jokes.csv")
  todays_joke = find_todays_joke(jokes)
  joke_setup = todays_joke['setup']
  joke_punchline = todays_joke['punchline']

  # Prepare contacts
  if runmode == 'test':
    contacts = get_csv_content("contacts_test.csv")
  else:
    contacts = get_csv_content("contacts.csv")
    
  # Prepare business slogans
  num_slogans = len(contacts)
  logger.debug(f'Retrieving {num_slogans} slogans')
  slogans_iterator = iter(get_random_slogans(num_slogans))
  
  # Prepare projects
  projects = get_random_projects(len(contacts))
  print(projects)

  # Send mail
  
  for i,contact in enumerate(contacts):
    slogan = next(slogans_iterator)
    recipient_name = contact['name']
    recipient_email = contact['email']
    
    if recipient_email == '':
      logger.error(f'Contact email for {recipient_name} cannot be blank. Skipping...')
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

    {joke_setup}
    {joke_punchline}

    Looking to start a new business? Consider this slogan!
    {slogan}
    
    Making friends can be hard! Here's a conversation starter to try today.
    {get_random_topic()}
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
          <strong>{joke_setup}</strong><br><br>
          <i>{joke_punchline}</i>
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
          <b>{get_random_topic()}</b>
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
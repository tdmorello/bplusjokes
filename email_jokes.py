import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import datetime
import logging
import sys
import argparse
from time import sleep

from get_random_slogan import get_random_slogan
from get_random_content import get_random_noun

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

  # Send mail
  
  for contact in contacts:
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
    Good day {recipient_name},
    Thank you for your irreversible subscription to Dog Joke of the Day.
    Here's your dog joke of the day!

    {joke_setup}
    {joke_punchline}

    Looking to start a new business? Consider this slogan!<br>
    {get_random_slogan(get_random_noun())}
    """

    html = f"""\
    <html>
      <body>
        <p>Good day {recipient_name},<br><br>
          Thank you for your irreversible subscription to Dog Joke of the Day.<br>
          Here's your dog joke of the day!
        </p>
        <br>
        <h1>#JokeSection</h1>
        <p>
          <strong>{joke_setup}</strong><br><br>
          <i>{joke_punchline}</i>
        </p>
        <br>
        <h1>#BusinessSection</h1>
        <p>
          Looking to start a new business? Consider this slogan!<br><br>
          <b>{get_random_slogan(get_random_noun())}</b>
        </p>
        <br><br>
        <p>
          Already have a Dog Joke of the Day provider?
          <a href="https://www.google.com/search?q=how+to+unsubscribe+from+dog+joke+of+the+day">Click here to unsubscribe</a>
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
      logger.debug(f'Email to {recipient_name} was sent.')
    except smtplib.SMTPRecipientsRefused as e:
      logger.error(f'RecipientsRefused: {recipient_name}: {e}')
    
    sleep(15)

  return None

if __name__ == '__main__':
    main()
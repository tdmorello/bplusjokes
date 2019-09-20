import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import datetime
import logging
import sys


logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(levelname)s : %(message)s')

# TODO:
# Add check that every joke has a send-date

def get_csv_content(csv_file):
  """Create ordered dictionary from a csv file content"""
  logging.debug(f"Getting content from {csv_file}")
  try:
    with open(csv_file, encoding='utf-8-sig') as csvfile:
      reader = csv.DictReader(csvfile)
      data = []
      for row in reader:
        data.append(row)
      logging.debug(f"Found {len(data)} entries in {csv_file}")
      return data
  except IOError as e:
    logging.error(msg = e)

def find_todays_joke(jokes):
  logging.debug("Finding today's joke.")
  for joke in jokes:
    entry_date = datetime.datetime.strptime(joke['send_date'], '%Y-%m-%d').date()
    if entry_date == datetime.date.today():
      logging.debug("Found today's joke.")
      logging.info(f"Today's joke is: {joke}")
      return joke
  
  logging.error("No jokes for today were found.")
  sys.exit()

def create_body_content(name = None, p1 = None, p2 = None, greeting = None, farewell = None):
  # TODO: fill this in
  return None

def main():
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
  contacts = get_csv_content("contacts.csv")

  for contact in contacts:
    recipient_name = contact['name']
    recipient_email = contact['email']

    logging.info(f"Sending email to {recipient_name} at {recipient_email}")

    # MESSAGE
    message = MIMEMultipart("alternative")
    message["Subject"] = f'J of the D: {joke_setup}'
    message["From"] = sender_name + ' <' + sender_email + '>'
    message["To"] = recipient_email

    # Create the plain-text and HTML version of your message
    text = f"""\
    Good day {recipient_name},
    Here's your dog joke of the day!

    {joke_setup}

    {joke_punchline}
    """

    html = f"""\
    <html>
      <body>
        <p>Good day {recipient_name},<br>
          Here's your dog joke of the day!<br><br>
          <strong>{joke_setup}</strong><br><br>
          <i>{joke_punchline}</i>
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

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(sender_email, password)
      server.sendmail(
          sender_email, recipient_email, message.as_string()
      )
    logging.debug(f'Email to {recipient_name} was sent.')

  return None

if __name__ == '__main__':
    main()
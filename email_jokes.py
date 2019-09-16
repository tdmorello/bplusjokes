import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import datetime

sender_email = "bplusjokes@gmail.com"
sender_name = "B+ Jokes"
# receiver_email = "tdmorello@gmail.com"
password = "epcjxgyzlmijdyui"

today = datetime.date.today()

with open("dog_jokes.csv") as file:
  reader = csv.reader(file)
  jokes = list(reader)

todays_joke = []
for entry in jokes:
  entry_date = datetime.datetime.strptime(entry[0], '%Y-%m-%d').date()
  if entry_date == today:
    todays_joke = entry[1:3]
    print(f"Today's joke is: {todays_joke}")
    break

with open("contacts_file.csv") as file:
  reader = csv.reader(file)
  for recipient_name, receiver_email in reader:
    print(f"Sending email to {recipient_name} at {receiver_email}")

    subject = f'J of the D: {todays_joke[0]}'

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_name + ' <' + sender_email + '>'
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = f"""\
    Good day {recipient_name},
    Here's your dog joke of the day!

    {todays_joke[0]}

    {todays_joke[1]}
    """

    html = f"""\
    <html>
      <body>
        <p>Good day {recipient_name},<br>
          Here's your dog joke of the day!<br><br>
          <strong>{todays_joke[0]}</strong><br><br>
          <i>{todays_joke[1]}</i>
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
          sender_email, receiver_email, message.as_string()
      )

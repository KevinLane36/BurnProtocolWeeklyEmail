import requests
from bs4 import BeautifulSoup
from decouple import config
from email.message import EmailMessage
import ssl
import smtplib

URL = "https://burnbootcamp.com/workout/protocol/"
page = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(page.content, "html.parser")

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
s = soup.find_all('div', class_='workout')
workout_list = []
i = 0
for line in s:
    workout_list.append(weekdays[i] + ' - ' + str(line).replace('<div class="workout">', "").replace('</div>', "").replace('[', '').replace(']', '').replace('\n', ''))
    i+=1

email_sender = 'burn.protocol.weekly@gmail.com'
EMAIL_PASS = config('EMAIL_PASS')
receiver_list = ['18287757588@mms.uscc.net','9196239163@vzwpix.com']

subject = 'Burn Protocol This Week'
body = str(workout_list).replace(',', '\n\n').replace("[", "").replace("]", "").replace("'", "")

context = ssl.create_default_context()
for email_receiver in receiver_list:
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, EMAIL_PASS)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
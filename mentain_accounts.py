import schedule
import time
import random
import smtplib
from email.mime.text import MIMEText
from essential_generators import DocumentGenerator
import json

import create_email_adress_yandex

def send_email():
    #chose random sender and reciever
    with open('generated_accounts.txt') as json_file:
        data = json.load(json_file)
    sender = random.choice(data["accounts"])
    sender_user =sender["username"] + "@yandex.com"
    sender_password = sender["password"]

    reciever_user = random.choice(data["accounts"])["username"] + "@yandex.com"

    #generate random body paragraph and send email
    gen = DocumentGenerator()
    body = gen.paragraph()
    msg = MIMEText(body)
    msg["Subject"] = gen.sentence()
    msg["From"] = sender_user
    msg["To"] = reciever_user

    s = smtplib.SMTP_SSL('smtp.yandex.ru',465)
    #idk what this does
    s.ehlo()
    #s.starttls()

    s.set_debuglevel(1)
    s.login(sender_user, sender_password)
    s.sendmail(sender_user, [reciever_user], msg.as_string())
    s.quit()
    print ("sent mail")

def write_review():
    pass

#create 1 email per day
schedule.every().day.at("02:00").do(create_email_adress_yandex.generate_multiple_accounts, 2)
#send 5 emails per day
schedule.every().day.at("03:00").do(send_email)
schedule.every().day.at("04:00").do(send_email)
schedule.every().day.at("05:00").do(send_email)
schedule.every().day.at("06:00").do(send_email)
#write one review per day
schedule.every().day.at("07:00").do(write_review)
schedule.every().day.at("08:00").do(write_review)
schedule.every().day.at("09:00").do(write_review)



send_email()
while True:
    schedule.run_pending()
    time.sleep(60)

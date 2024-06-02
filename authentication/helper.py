import random
import string
import secrets

#Emails

import smtplib
from datetime import datetime
from email.mime.text import MIMEText

import requests
import re


def validate_email(email_address):
    pattern = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    return bool(re.fullmatch(pattern, email_address))

def split_email(email):
    pattern = r"([^\s]+)@([^\s]+)"
    match = re.search(pattern, email)
    if match:
        return match.groups()
    else:
        return None

def gen_auth_code():
    letters = string.ascii_letters
    digits = string.digits
    selection_list = letters + digits

    password_len = 10

    password = ''
    for i in range(password_len):
        password += ''.join(secrets.choice(selection_list))

    return password


def send_msg(email, url):

    body = """
        Thanks for using PlantPal!
        Your verification url is: {url}
    """.format(url=url)
    subject = "PlantPal - Your verification URL"

    date_today = datetime.today().strftime('%m/%d/%Y')
    fromMy = "PlantPal@yahoo.com"

    smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
    smtp_ssl_port = 465
    username = 'demo.plantpal@gmail.com'
    password = 'vikb qglh csum zllu'
    sender = 'demo.plantpal@gmail.com'
    targets = [email]

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(targets)

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(username, password)
    server.sendmail(sender, targets, msg.as_string())
    server.quit()
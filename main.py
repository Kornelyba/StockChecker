import json
import time
import smtplib
import requests
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup
from email.message import EmailMessage

log = ""

##Make sure to edit the config.json file with your account information

def check_availability(url, phrase):
    global log
    try:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, features='html.parser')
        if phrase in soup.text:
            resp = requests.post('https://textbelt.com/text', {
                'phone': '5555555555',              ##OPTIONAL- enter a phone number to recieve text notifications
                'message': 'Your item is available',
                'key': 'textbelt',
            })
            print(resp.json())
            return False
        return True
    except:
        log += "Error parsing the website "


def main():
    global log
    url = "your site here" ##Enter the URL to the product page you'd like to check
    phrase = "Currently out of stock"
    available = check_availability(url, phrase)

    logfile = open('log.txt', 'r+')

    successMessage = "x seems to be available! " ##Enter the name of the item you wish to check

    if successMessage not in logfile.read():
        print("x is already found in stock ")    ##Enter the name of the item you wish to check
        return
    else:
        print("no item found")

    if available:
        log += successMessage
        try:
            with open('config.json') as file:
                config = json.load(file)
                username = config['username']
                password = config['password']
                fromAddress = config['fromAddress']
                toAddress = config['toAddress']
        finally:
            log += "Error with the credentials file "

        msg = EmailMessage()
        msg['Subject'] = "x is in stock! "       ##Enter the name of the item you wish to check
        msg['From'] = fromAddress
        msg['To'] = toAddress
        msg.set_content("It seems that there is a x available at " + url) ##Enter the name of the item you wish to check

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(username, password)

            server.send_message(msg)
            server.quit()
            log += "Message sent! "
        finally:
            log += "Error sending message "
    else:
        log += "No x available "  ##Enter the name of the item you wish to check
    logfile.write(str(datetime.now()) + " " + log + "\n")
    logfile.close()


while True:
    if __name__ == '__main__':
        main()
    time.sleep(60)

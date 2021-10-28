import argparse
import re
import smtplib
import ssl
from datetime import datetime

import requests
from bs4 import BeautifulSoup

def letterCheck(x):
    pattern = "^[a-zA-Z]$"
    regex = re.compile(pattern)
    if not regex.match(str(x)):
        raise argparse.ArgumentTypeError('--teacher parameter must be a valid letter a-z')
    return x


def catCheck(x):
    if int(float(x)) < 1:
        raise argparse.ArgumentTypeError('--cat-facts parameter must be a positive integer')
    return x


def send_mail(message, config):
    smtp_server = "smtp.gmail.com"
    port = 465
    login = "berkecengiz94@gmail.com"
    pw = config
    context = ssl.create_default_context()
    receiver_email = "wojciech.thomas@pwr.edu.pl"
    now = datetime.now()
    body_text = now.strftime("%Y-%m-%d %H:%M:%S") + "\n\n" + "Dear Professor," + "\n\t" + message

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(login, pw)
        server.sendmail(login, receiver_email, body_text)


def fetch_cats(this_many):
    base_url = 'https://cat-fact.herokuapp.com'
    facts_end = '/facts/random'
    url_path = base_url+facts_end
    amount = abs(int(float(this_many)))
    if amount < 1:
        print("number of facts requested must be greater than 0")
        exit(1)
    p = {'animal_type': 'cat', 'amount': amount}
    response = requests.get(url=url_path, params=p)
    data = response.json()

    print("Displaying Cat Facts: ")
    if amount > 1:
        cat_facts = [res['text'] for res in data]
        for fact in cat_facts:
            print("\n" + fact)
    elif amount == 1:
        print("\n" + data['text'])


def fetch_teachers(letter):
    base_url = 'https://wiz.pwr.edu.pl/pracownicy?letter=D.'
    p = {'letter': letter.upper()}
    page = requests.get(url=base_url, params=p)

    if page.status_code != 200:
        print("Error in getting page.")
        exit(1)

    the_soup = BeautifulSoup(page.content, 'html.parser')
    teacher_rows = the_soup.find_all('div', class_='col-text text-content')

    names = []
    emails = []
    for row in teacher_rows:
        for para in row.find_all('a', recursive=False):
            names.append(para.text)

    for row in teacher_rows:
        for p in row.select('p'):
            emails.append(p.text)

    teachers_data = dict(zip(names, emails))

    print("List of Researchers - " + letter.upper() + ":")
    for k,v in teachers_data.items():
        print("\n" + str(k) + "\n" + str(v))


def read_config():
    pw = ""
    file = open("config.json", 'r', encoding='utf-8')
    for line in file:
        pw = line
    file.close()
    return pw


def run():
    parser = argparse.ArgumentParser(description='Arg Parses')
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--mail", required=False, help="Enter message to send.")
    g.add_argument("--cat-facts", required=False, type=catCheck, help="Enter number of cat facts to display.")
    g.add_argument("--teachers", required=False,  type=letterCheck,
                   help="Enter letter to fetch researcher data for.")
    args = parser.parse_args()
    message_info = args.mail
    cat_num = args.cat_facts
    research_l = args.teachers

    if message_info is not None:
        config = read_config()
        send_mail(message_info, config)
    elif cat_num is not None:
        fetch_cats(cat_num)
    elif research_l is not None:
        fetch_teachers(research_l)


if __name__ == "__main__":
    run()
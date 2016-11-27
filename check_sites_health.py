import os
import sys
import requests
import whois
import datetime
from dateutil.relativedelta import relativedelta


def load_urls4check(path):
    if not os.path.exists(path):
        return None
    with open(path, 'r') as f:
        return f.read().split()


def is_server_respond_with_200(url):
    try:
        return requests.get(url).status_code == 200
    except:
        return False


def get_domain_expiration_date(domain_name):
    expiration_date = whois.whois(domain_name).expiration_date
    if type(expiration_date) == list:
        return expiration_date[0]
    return expiration_date


def is_available_month_later(domain_name):
    month_later = datetime.date.today() + relativedelta(months=+1)
    expired_date = get_domain_expiration_date(domain_name).date()
    return expired_date > month_later


if __name__ == '__main__':
    path = input("Please enter path to file with urls you want to check or type 'exit' to exit: ")
    urls = load_urls4check(path)
    if not urls:
        sys.exit("Incorrect path to file with urls.")
    for url in urls:
        if is_server_respond_with_200(url):
            text = '%s is available' % url
            if is_available_month_later:
                print(text, 'and domain is payed more than 1 month in advance.')
            else:
                print(text, 'and domain is NOT payed more than 1 month in advance or has been expired.' % url)
        else:
            print('%s is NOT available!' % url)

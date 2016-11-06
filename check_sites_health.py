import os
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
        if requests.get(url).status_code == 200:
            return True
        return False
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
    if expired_date < month_later:
        return False
    else:
        return True


if __name__ == '__main__':
    urls = load_urls4check(input("Please enter path to urls-file: "))
    if urls:
        for url in urls:
            if is_server_respond_with_200(url):
                print('%s is available.' % url)
                if is_available_month_later:
                    print('Domain name of %s is payed more than 1 month in advance.' % url)
                else:
                    print('Domain name of %s will be blocked in less than a month.' % url)
            else:
                print('%s is NOT available!' % url)
    else:
        print("Incorrect path to urls-file.")

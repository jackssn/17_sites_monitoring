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


def print_urls(url_list):
    if url_list:
        for i, url in enumerate(url_list):
            print("\t%s) %s" % (i+1, url))

if __name__ == '__main__':
    urls = load_urls4check(input("Please enter path to urls-file: "))
    if urls:
        available_urls = [url for url in urls if is_server_respond_with_200(url)]
        unavailable_urls = [url for url in set(urls).difference(available_urls)]
        payed_domains = [url for url in available_urls if is_available_month_later(url)]
        expired_domains = [url for url in set(available_urls).difference(payed_domains)]
        if available_urls:
            print("Available urls:")
            print_urls(available_urls)
        if payed_domains:
            print("These domains are payed more than 1 month in advance:")
            print_urls(payed_domains)
        if expired_domains:
            print("These domains ain\'t payed more than 1 month in advance or has been expired:")
            print_urls(expired_domains)
        if unavailable_urls:
            print("Unavailable urls:")
            print_urls(unavailable_urls)
    else:
        print("Incorrect path to urls-file.")

#!/usr/bin/python

from lxml import html
from io import BytesIO
import argparse
import requests
import gzip


def month_emails(filename, url):
    print(filename)
    response = requests.get(url + filename)
    if filename[-3:] == '.gz':
        contents = gzip.GzipFile(fileobj=BytesIO(response.content)).read()
    else:
        contents = response.content
    return contents


def main():
    parser = argparse.ArgumentParser(description='Fetch mailman archives')
    parser.add_argument('url', type=str, help='Mailman archive URL')
    parser.add_argument('--months', type=int, default=12,
                        help='Number of monthly archives to download')
    args = parser.parse_args()

    months = args.months
    url = args.url
    if (url[-1] != '/'):
        url = url + '/'
    listname = url.rsplit('/', 2)[-2]

    response = requests.get(url)
    tree = html.fromstring(response.text)

    filenames = tree.xpath('//table/tr/td[3]/a/@href')
    contents = []

    for filename in filenames:
        if (months > 0):
            contents.append(month_emails(filename, url).decode('utf-8'))
            months = months - 1

    contents.reverse()

    contents = "\n\n\n\n".join(contents)

    with open(listname + '.mbox', 'w') as filehandle:
        filehandle.write(contents)


if __name__ == '__main__':
    main()

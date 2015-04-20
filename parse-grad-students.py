#!/usr/bin/env python
""" Parse the Eng Phys website to get a current list of graduate students, their macid's and other info """

import os
from bs4 import BeautifulSoup as Bs4
import requests
import csv
import re
import logging
import sys

logger = logging.getLogger()
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

GRAD_LIST_URL = "http://engphys.mcmaster.ca/graduate-studies/list-of-students/"
PKL_FILE = "debug.pkl"
DEFAULT_DATA_CSV = 'students.csv'


name_re = re.compile(u"(?P<first>.*), (?P<last>.*)\s+\((?P<level>.*)\)", re.UNICODE)


def parse_name(line):
    # Parse the line for the interesting items
    m = re.match(name_re, line)
    if m is None:
        print("Parse error for name string: {}".format(line))
        return {}
    else:
        return m.groupdict()


def clean_text(txt):
    txt = re.sub(u'\xa0', ' ', txt)
    txt = re.sub(u'"', '', txt)
    return txt


def strip_row(row):
    row_data = {'first': None,
                'last': None,
                'level': None,
                'email': None,
                'supervisor': None,
                'room': None,
                'ext': None}
    data = [td for td in row.find_all("td")]
    name_dict = parse_name(clean_text(data[0].get_text()))
    row_data.update(name_dict)
    row_data['supervisor'] = clean_text(data[1].get_text())
    row_data['room'] = clean_text(data[2].get_text())
    row_data['ext'] = clean_text(data[3].get_text())
    row_data['email'] = clean_text(data[0].a['href'].split('mailto:')[1])
    return row_data


def main(options):
    # Handle DEBUG
    logger.info("Parsing Eng Phys Grad Students")

    if options.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug Enabled")

        pkl_file = os.path.join(os.path.dirname(__file__), PKL_FILE)
        if not os.path.exists(pkl_file):
            logger.debug("Debug HTML file does not exist, parsing web site")
            r = requests.get(GRAD_LIST_URL)
            html_text = r.text
            with open(pkl_file, 'w') as f:
                f.write(html_text)
        else:
            logger.debug("Reading Debug HTML file")
            with open(pkl_file, 'r') as f:
                html_text = f.read()
    else:
        logger.info("Parsing Web Site")
        r = requests.get(GRAD_LIST_URL)
        html_text = r.text

    bs = Bs4(html_text)
    # Student table
    students = bs.find(id="bottom_content").table

    if options.file is not None:
        filename = options.file
    else:
        filename = DEFAULT_DATA_CSV

    logger.info("Saving student data to {}".format(filename))
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, ["first", "last", "level", "email", "supervisor", "room", "ext"])
        writer.writeheader()
        for row in students.find_all("tr")[1:]:
            data = strip_row(row)
            writer.writerow(data)

    logger.info("Finished parsing student data")


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser('A web scraper to get the current list of Eng Phys grad students at Mac')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enables Debug mode, useful for devs to not hit the site over and over')
    parser.add_argument('-f', '--file', dest='file', default=None,
                        help="Sets the CSV file name to save the student info, defaults to 'students.csv'")
    options = parser.parse_args()

    main(options)

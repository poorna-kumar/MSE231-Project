#! /usr/bin/env python2.7

import tarfile
import os
import sys
import csv
import gzip
import argparse
import nltk.data
import re
from nltk.tokenize import RegexpTokenizer
from datetime import datetime
from bs4 import BeautifulSoup, SoupStrainer

cwd = os.getcwd()
data_dir = '../data/nyt_corpus/data'
parser = argparse.ArgumentParser()
parser.add_argument("year", help="the year of articles to count", type=int)
parser.add_argument("month", help="the month of the articles to count", type=int)
args = parser.parse_args()

year = args.year
month = args.month

words_m = frozenset(['he', 'his', 'him', 'himself', 'men', 'man', 'male'])
words_f = frozenset(['she', 'hers', 'her', 'herself', 'women', 'woman', 'female'])
words_b = frozenset(['financier', 'entrepreneur', 'broker', 'investor', 'accountant'])
words_h = frozenset(['doctor', 'nurse', 'physician', 'pharmacist', 'surgeon'])
words_t = frozenset(['scientist', 'engineer', 'chemist', 'biologist', 'physicist'])
words_a = frozenset(['artist', 'writer', 'musician', 'painter', 'singer'])
words_s = frozenset(['salesperson', 'receptionist', 'housekeeper', 'driver', 'cashier'])

words_all = words_m | words_f | words_b | words_h | words_t | words_a | words_s

guid_pattern =  re.compile('/([^/]*)\\.xml$')

sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
word_tokenizer = RegexpTokenizer(r'\w+')

sections_filter = frozenset(['Arts', 'Business', 'Front Page', 'Health', 'Science', 'Technology'])

def clean_str(s):
    return ' '.join(s.split())

def get_info_from_file(f_handle):
    # returns a list of online_sections (if any)
    # returns a list of paragraphs strings, each item is a paragraph from the article.

    content = f_handle.read()
    soup = BeautifulSoup(content, 'xml')

    try:
        sections = soup.find('meta', {'name': 'online_sections'})['content'].split(';')
        sections = [clean_str(x) for x in sections if clean_str(x) in sections_filter]
    except TypeError:
        sections = set()



    # Do stuff here to read the actual contents
    body_text = []
    try:
        body_xml = soup.find('block', class_='full_text').find_all('p')
        for paragraph in body_xml:
            body_text.append(unicode(clean_str(paragraph.string.strip())))
    except AttributeError: # if there is no full_text
        pass
 
    return sections, body_text

def clean_up(sentence):
    """
    """
    # Strip quotes
    sentence = sentence.replace("'"," ") #replaced with spaces, mostly for contractions
    sentence = sentence.replace('"','')

    # Lower case
    sentence = sentence.lower()

    return sentence


os.chdir(data_dir)
os.chdir(str(year))

start_time = datetime.now()
print 'Starting script (year=%s, month=%s):' % (year, month), start_time
tar = tarfile.open('%02d' % month + ".tgz", 'r')
counter = 0

full_dict = {section : dict.fromkeys(words_all, 0) for section in sections_filter | set(["All"])}

for tarinfo in tar:
    if not tarinfo.isfile():
        continue #ignore directories, links, etc.
    tarinfo_name = tarinfo.name
    # filtering here
    guid_match = guid_pattern.search(tarinfo_name)
    if guid_match is None:
        print "Can't find GUID from tarinfo %s" % tarinfo_name
        continue
    else:
        guid = guid_match.group(1)
    
    f_handle = tar.extractfile(tarinfo)
    if f_handle is None:
        continue # really does the same thing as the first if
    sections, content = get_info_from_file(f_handle)

    for paragraph in content:
        sentences = sentence_tokenizer.tokenize(paragraph)
        for sentence in sentences:
            sentence = clean_up(sentence)
            words = word_tokenizer.tokenize(sentence)
            for word in words:
                if word in words_all:
                    for section in sections:
                        full_dict[section][word] += 1
                    full_dict['All'][word] += 1

    counter += 1

    # DEBUG
    #if counter >= 100:
    #   break

tar.close()
os.chdir(cwd) # get back to original location
with open('wc_%s%02d.tsv' % (year, month), 'wb') as tsvfile:
    columns = ['Section', 'Month', 'Year']
    columns.extend(list(words_all))
    tsvwriter = csv.DictWriter(tsvfile, columns, delimiter="\t")
    #tsvwriter.writeheader()
    for section in full_dict:
        row = full_dict[section]
        row['Section'] = section
        row['Month'] = month
        row['Year'] = year
        tsvwriter.writerow(row)

print counter,"files proccessed", datetime.now()-start_time


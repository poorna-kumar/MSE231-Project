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

data_dir = '../data/nyt_corpus/data'
year = 2007
month = 1

words_m = frozenset(['he', 'his', 'him', 'himself', 'men', 'man', 'male'])
words_f = frozenset(['she', 'hers', 'her', 'herself', 'women', 'woman', 'female'])

guid_pattern =  re.compile('/([^/]*)\\.xml$')

sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
word_tokenizer = RegexpTokenizer(r'\w+')

def clean_str(s):
    return ' '.join(s.split())

def get_body_from_file(f_handle):
    # returns a list of paragraphs strings, each item is a paragraph from the article.

    strainer_head = SoupStrainer("body")

    content = f_handle.read()
    soup = BeautifulSoup(content, 'xml', parse_only=strainer_head)

    # Do stuff here to read the actual contents
    body_text = []
    try:
        body_xml = soup.find('block', class_='full_text').find_all('p')
        for paragraph in body_xml:
            body_text.append(unicode(clean_str(paragraph.string.strip())))
    except AttributeError: # if there is no full_text
        pass
 
    return body_text 

def clean_up(sentence):
    """
    """
    # Strip quotes
    sentence = sentence.replace("'"," ") #replaced with spaces, mostly for contractions
    sentence = sentence.replace('"','')

    # Lower case
    sentence = sentence.lower()

    return sentence


outfile = gzip.open('wc_%s%02d.out.gz' % (year, month), 'wb')
os.chdir(data_dir)
os.chdir(str(year))

start_time = datetime.now()
print 'Starting script (year=%s, month=%s):' % (year, month), start_time
tar = tarfile.open('%02d' % month + ".tgz", 'r')
counter = 0

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
    content = get_body_from_file(f_handle)

    count_m = 0
    count_f = 0
    for paragraph in content:
        sentences = sentence_tokenizer.tokenize(paragraph)
        for sentence in sentences:
            sentence = clean_up(sentence)
            words = word_tokenizer.tokenize(sentence)
            for word in words:
                if word in words_m:
                    count_m += 1
                elif word in words_f:
                    count_f += 1

    print >>outfile, "%s\t%d\t%d" % (guid, count_m, count_f) 
    counter += 1

    # DEBUG
    #if counter >= 100:
    #    break

tar.close()
outfile.close()
print counter,"files proccessed", datetime.now()-start_time


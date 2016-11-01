#! /usr/bin/env python2.7

import tarfile
import os
import sys
import csv
import gzip
import argparse
from datetime import datetime
from bs4 import BeautifulSoup, SoupStrainer

def clean_str(s):
    return ' '.join(s.split())

parser = argparse.ArgumentParser()
parser.add_argument("year", help="the year of articles to index", type=int)
parser.add_argument("month", help="the month of the articles to index", type=int)
args = parser.parse_args()

index_s = gzip.open('output/index_s_%s%02d.tsv.gz' % (args.year, args.month), 'w')
index_m = gzip.open('output/index_m_%s%02d.tsv.gz' % (args.year, args.month), 'w')
index_s_writer = csv.writer(index_s, delimiter='\t')
index_m_writer = csv.writer(index_m, delimiter='\t')

data_dir = '../../data/nyt_corpus/data'

tags_s = ['Guid', 'News_Desk', 'Publication_Date', 'Section']
# print '\t'.join(tags_s)
tags_m = {'Descriptors': SoupStrainer('classifier', {'class':'indexing_service', 'type':'descriptor'}),
          'General_Online_Descriptors': SoupStrainer('classifier', {'class':'online_producer', 'type':'general_descriptor'}),
          'Online_Descriptors': SoupStrainer('classifier', {'class':'online_producer', 'type':'descriptor'}),
          'Taxonomic_Classifiers': SoupStrainer('classifier', {'class':'online_producer', 'type':'taxonomic_classifier'}),
          'Names': SoupStrainer('classifier', {'class':'indexing_service', 'type':'names'}),
          'People': SoupStrainer('person', {'class':'indexing_service'}),
          'Online_People': SoupStrainer('person', {'class':'online_producer'}),
          'Locations': SoupStrainer('location', {'class':'indexing_service'}),
          'Online_Locations': SoupStrainer('location', {'class':'online_producer'})}
tags_ml = tags_m.keys()
tags_ml.append("Online_Sections")
#print '\n'.join(["%d\t%s" % x for x in enumerate(tags_ml)])

strainer_head = SoupStrainer("head")

os.chdir(data_dir)
os.chdir(str(args.year))

start_time = datetime.now()
print 'Starting script (year=%s, month=%s):' % (args.year, args.month), start_time
tar = tarfile.open('%02d' % args.month + ".tgz", 'r')
counter = 0
for tarinfo in tar:
    if not tarinfo.isfile():
        continue #ignore directories, links, etc.
    f_handle = tar.extractfile(tarinfo)
    if f_handle is None:
        continue # really does the same thing as the first if
    content = f_handle.read()
    soup = BeautifulSoup(content, 'xml', parse_only=strainer_head)
    # print content
    docdata = {}
    # data in all articles
    docdata['Guid'] =  clean_str(soup.find('doc-id')['id-string'])
    docdata['News_Desk'] = clean_str(soup.find('meta', {'name': 'dsk'})['content'])
    docdata['Publication_Date'] = clean_str(soup.find('pubdata')['date.publication'])[:8] #slice first 8 characters for YYYYMMDD
    docdata['Section'] = clean_str(soup.find('meta', {'name':'print_section'})['content'])
    # single stuff
    try:
        sections = soup.find('meta', {'name': 'online_sections'})['content'].split(';')
        sections = [clean_str(x) for x in sections]
        docdata['Online_Section'] = sections
    except TypeError:
        docdata['Online_Section'] = []

    # indecies with multiple values:
    soup_m = soup.find('identified-content')
    for tag in tags_m:
        docdata[tag] = []
        try:
            for field in soup_m.find_all(tags_m[tag]):
                docdata[tag].append(unicode(clean_str(field.string)).strip())
        except TypeError:
            pass

    list_to_print = [docdata[x] for x in tags_s]
    #print 'Single:','\t'.join(list_to_print)
    index_s_writer.writerow(list_to_print)

    for i,tag in enumerate(tags_m):
        for field in docdata[tag]:
            # print 'Multi:','\t'.join([docdata['Guid'], field, str(i)])
            index_m_writer.writerow([docdata['Guid'], field.encode('utf-8'), str(i)])

    # print docdata
    counter += 1
#    if not counter % 1000:
#        print counter,'files processed:', datetime.now()-start_time
#    if counter >= 10:
#        break
tar.close()
index_s.close()
index_m.close()
print counter,"files proccessed", datetime.now()-start_time

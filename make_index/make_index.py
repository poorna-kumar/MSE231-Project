#! /usr/bin/env python2.7

import tarfile
import os
import sys
import csv
import gzip
import argparse
from bs4 import BeautifulSoup, SoupStrainer

index_s = gzip.open('index.tsv.gz', 'w')
index_m = gzip.open('index_m.tsv.gz', 'w')
index_s_writer = csv.writer(index_s, delimiter='\t')
index_m_writer = csv.writer(index_m, delimiter='\t')

data_dir = '../../data/nyt_corpus/data'
years = [2000]
months = range(1, 12+1)
os.chdir(data_dir)
os.chdir(str(years[0]))
#print os.getcwd() #sanity check

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

for month in [1]: #test is with first month
    tar = tarfile.open('%02d' % month + ".tgz", 'r')
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
        docdata['Guid'] =  soup.find('doc-id')['id-string']
        docdata['News_Desk'] = soup.find('meta', {'name': 'dsk'})['content']
        docdata['Publication_Date'] = soup.find('pubdata')['date.publication'][:8] #slice first 8 characters for YYYYMMDD
        docdata['Section'] = soup.find('meta', {'name':'print_section'})['content']
        # single stuff
        try:
            sections = soup.find('meta', {'name': 'online_sections'})['content'].split(';')
            sections = [x.strip() for x in sections]
            docdata['Online_Section'] = sections
        except TypeError:
            docdata['Online_Section'] = []

        # indecies with multiple values:
        for tag in tags_m:
            docdata[tag] = []
            try:
                for field in soup.find_all(tags_m[tag]):
                    docdata[tag].append(unicode(field.string))
            except TypeError:
                pass
        

        list_to_print = [docdata[x] for x in tags_s]
        #print 'Single:','\t'.join(list_to_print)
        index_s_writer.writerow(list_to_print)

        for i,tag in enumerate(tags_m):
            for field in docdata[tag]:
                # print 'Multi:','\t'.join([docdata['Guid'], field, str(i)])
                index_m_writer.writerow([docdata['Guid'], field, str(i)])

        # print docdata
        counter += 1
        if counter >= 10:
            break
    tar.close()
    print counter,"files proccessed"

index_s.close()
index_m.close()
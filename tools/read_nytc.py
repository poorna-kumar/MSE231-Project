#! /usr/bin/env python2.7

import tarfile
import os
import sys
from bs4 import BeautifulSoup, SoupStrainer

def clean_str(s):
    return ' '.join(s.split())

def get_body_from_file(f_handle):
    # returns a list of paragraphs strings, each item is a paragraph from the article.

    strainer_head = SoupStrainer("body")

    content = f_handle.read()
    soup = BeautifulSoup(content, 'xml', parse_only=strainer_head)

    # Do stuff here to read the actual contents
    body_xml = soup.find('block', class_='full_text').find_all('p')
    body_text = []
    for paragraph in body_xml:
        body_text.append(unicode(clean_str(paragraph.string.strip())))

    return body_text    

def get_article(guid, year, month, day, from_tar=True):
    """Returns the body of the article as a string, given it's guid.

    Currently requires year, and month, as index_checking isn't implemented.
    """
    data_dir = '../data/nyt_corpus/data'

    os.chdir(data_dir)
    os.chdir(str(year))

    if from_tar:
        tar = tarfile.open('%02d' % month + ".tgz", 'r')
        member_name = '%02d/%02d/%7d.xml' % (month, day, guid) 
        try:
            tarinfo = tar.getmember(member_name)
        except KeyError:
            print member_name
            raise KeyError('article (GUID: %d) not found on %4d/%02d/%02d' % (guid, year, month, day))

        if not tarinfo.isfile():
            raise KeyError('Invalid file in .tgz file')

        f_handle = tar.extractfile(tarinfo)
        if f_handle is None:
            raise KeyError('Cannot extract xml file in .tgz file')
    else:
        os.chdir(str(month))
        os.chdir(str(day))
        f_handle = open('%7d.xml' % guid)


    body_text = get_body_from_file(f_handle)

    # cleanup
    if from_tar:
        tar.close()
    else:
        f_handle.close()

    return '\n'.join(body_text)

def main():
    # Tests the get body text function
    text = get_article(1815799, 2007,1,1) 
    print text

if __name__ == '__main__':
    main()

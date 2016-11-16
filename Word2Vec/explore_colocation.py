import glob, os
import gensim
from bs4 import BeautifulSoup
import nltk.data
import argparse
from nltk.tokenize import RegexpTokenizer

sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
word_tokenizer = RegexpTokenizer(r'\w+')

def file_to_soup(filename):
    """
    """
    html_report_part1 = open(filename,'r')
    soup = BeautifulSoup(html_report_part1, "xml")
    return soup

def clean_up(sentence):
    """
    """
    # Strip quotes
    sentence = sentence.replace("'","")
    sentence = sentence.replace('"','')

    # Lower case
    sentence = sentence.lower()

    return sentence

def find_sentences(dir_path,w1,w2):
    article_count = 0
    hit_count = 0
    # Change directory to specified path
    os.chdir(dir_path)
    # Walk through files
    for root, dirs, files in os.walk("."):
        path = root.split('/')
        for file in files:
            # Open only xml files
            if file.endswith(".xml"):
                # Count article
                article_count = article_count + 1

                # Convert file to soup
                soup = file_to_soup("./" + str("/".join(path)) + "/" + str(file))

                # Obtain body content
                contents =  soup.find_all("body.content")
                for content in contents:
                    # Obtain blocks of content
                    blocks = content.find_all("block")
                    for block in blocks:
                        # Only get full text
                        if str(block['class']) != "full_text":
                            continue
                        # Obtain paragraphs of content
                        paragraphs = block.find_all("p")
                        for p in paragraphs:
                            p = str(p).replace("<p>","").replace("</p>","")
                            try:
                                sentences = sentence_tokenizer.tokenize(p)
                                for sentence in sentences:
                                    sentence = clean_up(sentence)
                                    words = word_tokenizer.tokenize(sentence)
                                    if w1 in words and w2 in words:
                                        print words
                                        hit_count = hit_count + 1
                            except UnicodeDecodeError:
                                pass
    print article_count
    print hit_count

# Parse arguments
parser = argparse.ArgumentParser(description='Evaluate accuracy')
parser.add_argument('-d','--doc_path', action="store", default = False)
parser.add_argument('-w1','--word1', action="store", default = False)
parser.add_argument('-w2','--word2', action="store", default = False)
args = vars(parser.parse_args())

# Print sentences
find_sentences(args['doc_path'],args['word1'],args['word2'])
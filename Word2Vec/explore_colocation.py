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

def any_in(l1,l2):
    """
    """
    return any(i in l1 for i in l2)

def find_sentences(dir_path,w1,w2):
    # Split words into lists
    w1 = w1.split()
    w2 = w2.split()

    # Set-up tracking variables
    article_count = 0
    w1_count = [0]*len(w1)

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
                                    if any_in(w1,words) and any_in(w2,words):
                                        for i, w1_word in enumerate(w1):
                                            if w1_word in words:
                                                print w1_word
                                                w1_count[i] = w1_count[i] + 1 
                            except UnicodeDecodeError:
                                pass
    print article_count
    print w1_count

# Parse arguments
parser = argparse.ArgumentParser(description='Evaluate accuracy')
parser.add_argument('-d','--doc_path', action="store", default = False)
parser.add_argument('-w1','--words1', action="store", default = False)
parser.add_argument('-w2','--words2', action="store", default = False)
args = vars(parser.parse_args())

# Print sentences
find_sentences(args['doc_path'],args['words1'],args['words2'])
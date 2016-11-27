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

class ArticleSentences(object):
    """
    """
    def __init__(self, dirname, file_set):
        self.dirname = dirname
        self.file_set = file_set
 
    def __iter__(self):
        # Change directory to specified path
        os.chdir(self.dirname)
        # Walk through files
        for root, dirs, files in os.walk("."):
            path = root.split('/')
            for file in files:
                # Open only xml files
                if file.endswith(".xml"):
                    # Convert file to soup
                    soup = file_to_soup("./" + str("/".join(path)) + "/" + str(file))

                    # Check that document has correct author gender
                    if file not in file_set:
                        continue

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
                                        yield word_tokenizer.tokenize(sentence)
                                except UnicodeDecodeError:
                                    pass

# Parse arguments
parser = argparse.ArgumentParser(description='Evaluate accuracy')
parser.add_argument('-d','--doc_path', action="store", default = False)
parser.add_argument('-m','--model_file', action="store", default = False)
parser.add_argument('-af','--author_file', action="store", default = False)
parser.add_argument('-as','--author_sex_desired', action="store", default = False)
args = vars(parser.parse_args())

# Get set of relevant documents
with open(args['author_file']) as f:
    content = f.readlines()

file_list = []
for line in content:
    if line.split("\t")[1].strip() == args['author_sex_desired']:
        file_list.append(line.split("\t")[0].strip()) 
file_set = set(file_list)

# Build word2vec model
## Test save - to make sure you didn't screw something up
model = gensim.models.Word2Vec(iter=1)
model.save(args['model_file'])

## Build model
sentences = ArticleSentences(args['doc_path'], file_set)
model = gensim.models.Word2Vec(sentences)

## Save model
model.save(args['model_file'])
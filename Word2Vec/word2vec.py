import glob, os
import gensim
from bs4 import BeautifulSoup
import nltk.data

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def file_to_soup(filename):
    """
    """
    html_report_part1 = open(filename,'r')
    soup = BeautifulSoup(html_report_part1, "xml")
    return soup

def soup_to_sentences(soup):
    """
    """
    sentence_list = []
    contents =  soup.find_all("body.content")
    for content in contents:
        blocks = content.find_all("block")
        for block in blocks:
            if str(block['class']) == "full_text":
                paragraphs = block.find_all("p")
                for p in paragraphs:
                    p = str(p).replace("<p>","").replace("</p>","")
                    try:
                        sentences = tokenizer.tokenize(p)
                        for sentence in sentences:
                            sentence_list.append(sentence.split())
                    except UnicodeDecodeError:
                        pass
    return sentence_list

# Set-up sentences
os.chdir("/Users/jmoore523/Documents/NYT_Test/")
sentences = []
for root, dirs, files in os.walk("."):
    path = root.split('/')
    for file in files:
        if file.endswith(".xml"):
            soup = file_to_soup("./" + str("/".join(path)) + "/" + str(file))
            for element in soup_to_sentences(soup):
                sentences.append(element)

# Build word2vec model
model = gensim.models.Word2Vec(sentences)

# Test word2vec model
print "Similarlity: Woman & Man"
print model.similarity('woman', 'man')
print "Similarlity: Even & Odd"
print model.similarity('even', 'odd')
print "Similarlity: Shoe & Business"
print model.similarity('shoe', 'business')
print "Similarlity: Business & Woman"
print model.similarity('business', 'woman')
print "Similarlity: Business & Revenue"
print model.similarity('business', 'revenue')
print "Similarlity: Job & Career"
print model.similarity('job', 'career')

print "Similarlity: She & Strong"
print model.similarity('she', 'strong')
print "Similarlity: She & Weak"
print model.similarity('she', 'weak')

print "Similarlity: He & Strong"
print model.similarity('he', 'strong')
print "Similarlity: He & Weak"
print model.similarity('he', 'weak')
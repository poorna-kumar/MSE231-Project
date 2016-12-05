import sys
from annotate_utils import annotate_corenlp
import xml.etree.ElementTree as xml
from os import walk
from os.path import join
from collections import defaultdict
import pprint
from operator import itemgetter

def discardArticle(section, discardSet):
    if "Science" not in section and "Technology" not in section:
        return True
    for el in discardSet:
        if el in section:
            return True
    return False

def wordIsPronoun(word):
    return word['pos'] in ['PRP', 'PRP$'] #Should always be PRP$, I think

if __name__ == '__main__':

    datadir = "../data/2006/"

    #Discard set
    discardSet = set(['Opinion', 'Style', 'Corrections'])
    
    #Dependency dictionary, consists of a dictionary for male words and one for female words. Maps possessions to counts. 
    depDict = {'male':{}, 'female':{}}
    
    for root_dir, dirs, files in walk(datadir):
        print "In:", root_dir
        for f in files:
            if not f.endswith('xml'):
                continue
            full_f = join(root_dir, f)
            e = xml.parse(full_f)
            root = e.getroot()
            #### Get section
            try:
                section = root.findall(".//meta[@name='online_sections']")[0].attrib['content']
            except:
                section = ""
            #### Decide whether to discard article
            if discardArticle(section, discardSet):
                continue                
            #### Get content
            try:
                content = root.findall(".//body.content/block[@class='full_text']")[0]
                content = '\n'.join([el.text for el in content])
            except IndexError:
                content = ""
            if content=="":
                continue

            #CoreNLP complains is content is not ascii (if it is unicode)
            if not isinstance(content, str):
                content = content.encode('ascii', 'ignore')
            
            annotation = annotate_corenlp(content, annotators = ['depparse', 'pos', 'lemma'])
                              
            for sentence in annotation['sentences']:
                accounted_deps = set()
                for word in sentence['tokens']:
                    gend = None
                    if wordIsPronoun(word):  
                        if word['lemma'] == 'he':
                            gend = 'male'
                        elif word['lemma'] == 'she':
                            gend = 'female'
                    if gend is not None:
                        for (dep_i, dep) in enumerate(sentence['basic-dependencies']):
                            #For every word, we are iterating through all deps
                            #Consider: "Her wit and her humor stand out."
                            #Contains two possessive links.
                            #We want to count each one only once, so we keep track ofaccounted deps.
                            if dep_i in accounted_deps:
                                continue
                            if dep['dep'] == 'nmod:poss':
                                accounted_deps.add(dep_i)
                                if dep['dependentGloss'] == word['word']:
                                    possession = dep['governorGloss']
                                    if possession in depDict[gend]:
                                        depDict[gend][possession] += 1
                                    else:
                                        depDict[gend][possession] = 1
    depDictMaleTuple = sorted(depDict['male'].items(), key = itemgetter(1), reverse = True)
    depDictFemaleTuple = sorted(depDict['female'].items(), key = itemgetter(1), reverse = True)
    pprint.pprint(depDictMaleTuple[0:30])
    pprint.pprint(depDictFemaleTuple[0:30])
    

import xml.etree.ElementTree as xml
from os import listdir
from os.path import isfile, join, isdir
import sys
sys.path.append('gender-from-name/')
import gender
import string

def get_gender(name):
    if name==None:
        return "unk"
    if name.upper() in gender.gender:
        return gender.gender[name.upper()]
    else:
        return "unk"

def get_name(byline, norm, filename):
    if byline == None or byline == "":
        return None, "no_byline"
    if norm == True:
        if "," in byline:
            first_name = byline.strip().split(',')[1]
            name = first_name.split()[0]
            if len(name) == 1:
                if len(first_name.split())>1: 
                    middle_name = first_name.split()[1]
                    if len(middle_name)==1:
                        return None, 'norm_only_initials'
                    else:
                        name = middle_name 
            return name, 'norm_looks_good'
        else:
            name = byline.strip().split()[0]
            return name, 'norm_no_comma'
    if norm == False:
        try:
            byline.translate(None, string.punctuation) #remove punctuation
        except:
            #print "Troublesome byline:", byline
            byline = byline.encode('ascii', 'ignore')
            #print "It has been converted to:", byline
        tokens = [e.lower() for e in byline.strip().split()] #lowercase tokens
        for i, token in enumerate(tokens):
            if token == 'by':
                try:
                    name = tokens[i+1]
                except IndexError:
                    return None, 'unnorm_no_name'
                return name, 'unnorm_regular'
        return tokens[0], 'unnorm_no_by'

if __name__ == '__main__':
    datadir = 'data/'
    ### Counters ###
    countFiles = 0
    ##############  
    bylineStatus = {'no_byline':0, 'norm_only_initials':0, 'norm_looks_good':0, 'norm_no_comma':0,\
                    'unnorm_no_name':0, 'unnorm_regular':0, 'unnorm_no_by':0}
    ##############
    years = [join(datadir, folder) for folder in listdir(datadir) if isdir(join(datadir, folder))]
    for year in years[1:]:
        year_name = year.split('/')[-1]
        f_write = open(year_name + '_gender_of_writer.tsv', 'w')
        months = [join(year, folder) for folder in listdir(year) if isdir(join(year, folder))]
        for month in months:
            print "Currently in folder:", month
            days = [join(month, f) for f in listdir(month) if isdir(join(month, f))]
            for day in days:
                files_in_day = [join(day, f) for f in listdir(day) if isfile(join(day, f))\
                               and f.endswith('.xml')]
                for f in files_in_day:
                    countFiles = countFiles + 1
                    e = xml.parse(f)
                    root = e.getroot()
                    #Byline
                    isBylineNorm = True
                    try:
                        norm_byline = root.findall(".//byline[@class='normalized_byline']")[0].text 
                        byline = norm_byline
                    except IndexError:
                        isBylineNorm = False
                        try:
                            byline = root.findall(".//byline[@class='print_byline']")[0].text
                        except IndexError:
                            byline = ""
                    name, status = get_name(byline, isBylineNorm, f)
                    bylineGender = get_gender(name)
                    filename = f.split('/')[-1]
                    if isinstance(bylineGender, (str, unicode)): #If gender is a string
                        f_write.write(filename + '\t' + bylineGender + '\n')
                    else: #If gender is a tuple
                        f_write.write(filename + '\t' + 'unk' + '\n')
        f_write.close()  

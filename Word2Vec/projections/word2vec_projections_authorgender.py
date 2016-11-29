from gensim.models import Word2Vec
from numpy import dot
from numpy.linalg import norm

years = [1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 2006]

# Identify words to be compared
gender_words = ['man','woman','he','she']
words = {'business' : ['financier','entrepreneur','broker','investor','accountant'], 
         'health' : ['doctor','nurse','physician','pharmacist','surgeon'],
         'science&tech' : ['scientist','engineer','chemist','biologist','physicist'],
         'arts' : ['artist','writer','musician','painter','singer'],
         'service' : ['salesperson','receptionist','housekeeper','driver','cashier'],
         'neutral' : ['person','human','somebody','someone'],
         'litcomp' : ['architect','captain','philosopher','hero','legend','aide','correspondent','chef','patron','comic','nurse','librarian','nanny','stylist','dancer']}

# Print headers
headers = ['year','author_gender','topic','word_diff','word','similarity']
print "\t".join(headers)

# Loop through each year
for year in years:
    for author_gender in ['M','F']:
        # Load model
        model = Word2Vec.load("/Volumes/My Book/W2VModels/GenderModels/{}{}.w2v".format(year,author_gender))

        he_she = model['he'] - model['she']
        he_she_norm = norm(he_she)
        man_woman = model['man'] - model['woman']
        man_woman_norm = norm(man_woman)

        for topic in words.keys():
            for word in words[topic]:
                word_vec = model[word]
                word_vec_norm = norm(model[word])

                # He-She
                w2vinfo = []
                w2vinfo.append(year)
                w2vinfo.append(author_gender)
                w2vinfo.append(topic)
                w2vinfo.append('He-She')
                w2vinfo.append(word)

                ## Calculate projection
                similarity = dot(he_she, model[word])/(he_she_norm * word_vec_norm)
                w2vinfo.append(similarity)

                w2vinfo = [str(x) for x in w2vinfo]
                print "\t".join(w2vinfo)

                # Man-Woman
                w2vinfo = []
                w2vinfo.append(year)
                w2vinfo.append(author_gender)
                w2vinfo.append(topic)
                w2vinfo.append('Man-Woman')
                w2vinfo.append(word)

                ## Calculate projection
                similarity = dot(man_woman, model[word])/(man_woman_norm * word_vec_norm)
                w2vinfo.append(similarity)
                
                w2vinfo = [str(x) for x in w2vinfo]
                print "\t".join(w2vinfo)

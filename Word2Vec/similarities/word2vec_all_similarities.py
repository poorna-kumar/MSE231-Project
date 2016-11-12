from gensim.models import Word2Vec

years = range(1987,2007)

# Identify words to be compared
gender_words = ['man','woman','he','she']
words = {'business' : ['financier','entrepreneur','broker','investor'], 
         'education' : ['teacher','educator','professor','nanny'],
         'science&tech' : ['scientist','programmer','chemist','biologist','physicist']}

# Print headers
headers = ['year','topic','gender_word','word','similarity']
print "\t".join(headers)

# Loop through each year
for year in years:
    # Load model
    model = Word2Vec.load("/Volumes/My Book/W2VModels/{}all.w2v".format(year))

    # Compute gender vector: man-woman
    # todo

    # Compute gender vector: he-she
    # todo

    for topic in words.keys():
        for word in words[topic]:   
            # Compare to gender vector: man-woman
            # todo

            # Compare to gender vector: he-she
            # to do

            for gender_word in gender_words:    

                # Initialize info vector
                w2vinfo = []
                w2vinfo.append(year)

                # Add word info
                w2vinfo.append(topic)
                w2vinfo.append(gender_word)
                w2vinfo.append(word)

                # Add similarity info
                w2vinfo.append(model.similarity(gender_word,word))           

                # Output data
                w2vinfo = [str(x) for x in w2vinfo]
                print "\t".join(w2vinfo)
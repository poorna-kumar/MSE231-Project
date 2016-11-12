from gensim.models import Word2Vec

years = range(1987,2007)
topics = ['Business','Technology','Health','Science']

gender_words = ['man','woman','he','she']
words = ['woman','leader','manager','father','mother','strong','weak']

headers = ['topic','year','vocabulary']
for gender_word in gender_words:
    for word in words:
        headers.append(gender_word + '_' + word)
print "\t".join(headers)

for topic in topics:
    for year in years:
        model = Word2Vec.load("/Volumes/My Book/W2VModels/{}{}.w2v".format(year, topic))

        # Initialize info vector
        w2vinfo = []
        w2vinfo.append(topic)
        w2vinfo.append(year)

        # Vocabulary size
        w2vinfo.append(len(model.vocab))

        # Word similarity
        for gender_word in gender_words:
            for word in words:
                w2vinfo.append(model.similarity(gender_word,word))           

        # Output data
        w2vinfo = [str(x) for x in w2vinfo]
        print "\t".join(w2vinfo)
from pycorenlp import StanfordCoreNLP


def annotate_corenlp(text, annotators=['pos'], output_format='json', port=9000):
    """
    Helper function to get the CoreNLP output.
    Usage:
    You need to install pycorenlp (using pip install corenlp) and have your
    StanfordCoreNLP server running on port (default 9000) using the instructions
    at http://stanfordnlp.github.io/CoreNLP/corenlp-server.html
    Arguments:
        text: the string with the text that you want to annotate.
        annotators: a list of CoreNLP annotators that you want it to run.
        (The table with all the annotators can be found at
        http://stanfordnlp.github.io/CoreNLP/annotators.html. You just need to
        put the property name from that table into this list. (Ex: 'pos', 'ner')
    """

    nlp = StanfordCoreNLP('http://localhost:{}'.format(port))
    return nlp.annotate(text, properties={
        'annotators': ','.join(annotators),
        'outputFormat': output_format
        })

import requests
import nltk
import nltk.tag.stanford as st

#Check if Message is Person Name
def checkPerson(message):
    tagger = st.StanfordNERTagger('stanford-ner-2015-04-20\classifiers\english.all.3class.distsim.crf.ser.gz', 'stanford-ner.jar')
    for sent in nltk.sent_tokenize(message.content.capitalize()):
        tokens = nltk.tokenize.word_tokenize(sent)
        tags = tagger.tag(tokens)
        for tag in tags:
            if tag[1] == 'PERSON':
                return message.content
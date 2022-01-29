 
import stanza
import os
from os.path import expanduser

nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse')

def find_svo(text):
    global nlp
    home = expanduser("~")
    if (not os.path.exists(home + '/stanza_resources')):
        stanza.download()
    
    doc = nlp(text)
    vo = []
    compound = True
    for sent in doc.sentences:
        for word in sent.words:
            if(word.upos == 'VERB' and word.deprel == 'xcomp'):
                print(word.text,word.deprel)
                vo.append(word.text)
            elif(word.upos == 'NOUN' and word.deprel == 'obj'):
                print(word.text,word.deprel)
                vo.append(word.text)
            elif(word.upos == 'NOUN' and word.deprel == 'compound'):
                print(word.text,word.deprel)
                vo.append(word.text)
            elif(word.upos == 'NOUN' and word.deprel == 'root' and compound):
                compound = False
                print(word.text,word.deprel)
                vo.append(word.text)

    return vo


# find_svo('I want you to mow my lawn')
# find_svo('I need my lawn mowed')
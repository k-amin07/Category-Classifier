from SVO import find_svo
with open('./train.txt','r') as train_file:
    lines = train_file.readlines()

def process_line(sentence,category):
    vo = find_svo(sentence)
    if(len(vo)<2):
        new_sentence = sentence
    else:
        new_sentence = ' '.join(vo)
    new_sentence.strip()
    with open('train_svo','a+') as svo_file:
        svo_file.write(new_sentence + ',' + category + '\n')

for line in lines:
    if(not lines.index(line)):
        with open('./train_svo','a+') as svo_file:
            svo_file.write(line)
        continue
    line = line.strip()
    line = line.lower()
    sentence,category = line.split(',')
    if('/' in sentence):
        #my fridge/refrigerators is broken
        sentence1,sentence2 = sentence.split('/')
        sentence1_new = sentence1 + ' ' +  ' '.join(sentence2.split(' ')[1:])
        sentence2_new = ' '.join(sentence1.split(' ')[:-1]) + ' ' +  sentence2
        process_line(sentence1_new,category)
        process_line(sentence2_new,category)
    else:
        process_line(sentence,category)
    

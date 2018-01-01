'''


        STEMMING DATA SET
        
'''


import pandas as pd
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import json
import string
import requests
import time

data_table = pd.read_csv('lyrics_dataset.csv', delimiter = '\t')


ps = PorterStemmer() # stemming
stop_en = get_stop_words('english')
stop_fr = get_stop_words('french')
stop_it = get_stop_words('italian')
stop_sp = get_stop_words('spanish')
stop_po = get_stop_words('portuguese')
stop_da = get_stop_words('german')
stop_ru = get_stop_words('russian')
all_stop = stop_sp + stop_it + stop_en + stop_fr + stop_po + stop_da # need stopwords for all song languages
all_stop = set(all_stop)

stemmed_lyrics = {}

x = 0

for lyrics in data_table['Lyrics'].values:    #per ogni testo di canzone
    lyrics = ''.join(char for char in str(lyrics) if char not in string.punctuation).lower().split()
                 #tolgo la punteggiatura, splitto le parole e utilizzo i caratteri minuscoli
    
    for word in lyrics:         #per ogni parola ndento al testo
        if word in all_stop:    #elimino le stop-words
            lyrics = lyrics[:lyrics.index(word)]+lyrics[(lyrics.index(word)+1):]
    lyrics = [ps.stem(word) for word in lyrics]  #utilizzo la funzione per le desinenze
    stemmed_lyrics[x] = lyrics      #associo il testo stemmato all'indice x della canzone
    x += 1


json.dump(stemmed_lyrics, open('stemmed_lyrics.json','w'))


'''

        DATA SET TOT
        
'''

#stemmed_lyrics= json.loads(open('stemmed_lyrics.json', 'r').read())
#data_table = pd.read_csv('lyrics_dataset.csv', delimiter = '\t')


x = 0
tot = {}
for item in data_table[['Title', 'Artist', 'Url', 'Lyrics']].values:
    tot[x] = {}
    tot[x]['id']=x
    tot[x]['Title'] = item[0]
    tot[x]['Artist'] = item[1]
    tot[x]['Url'] = item[2]
    tot[x]['Lyrics'] = stemmed_lyrics[x]
    x += 1
    
json.dump(tot, open('tot.json','w'))



'''

        POSTING LIST
        
'''

stemmed_lyrics= json.loads(open('stemmed_lyrics.json', 'r').read())


list_tf = {} # dict with key = word, attributes = dict([song], n_occurrencies)
n_word = {}  # dict with key = word, attribute = incremental

seen_words_post = set() # set where i will watch if words is already in the dictionary
i = 0

for song in stemmed_lyrics.keys():
    song_words = set() # NEED ANOTHER SET! I have to say if a word in song appear 2 or more time 
    for word in stemmed_lyrics[song]:
        word = str(word)
        # FIRST STEP: If i've got no presence of the word, create a key and append [doc, 1]
        # If not in seen_words_post, FOR SURE will not be in song_words
        if word not in seen_words_post:
            n_word[word] = i
            list_tf[word] = {}
            list_tf[word][song] = 1
            song_words.add(word)
            seen_words_post.add(word)
            i += 1
        # SECOND STEP: If word already seen before in other songs, but not in current song, add a key in the nested dict
        elif word not in song_words:
            list_tf[word][song] = 1
            song_words.add(word)
        # THIRD STEP: If word already in dict of dict, just add 1
        else:
            list_tf[word][song] += 1

    
json.dump(list_tf, open('list_tf.json','w'))
json.dump(n_word, open('n_word.json','w'))



'''

            DATA SET TO AND FROM MLAB
            
'''

######################################################################################################################################          UPLOAD    #####################################################
############################################################################################################


params = {'apiKey': 'hyWayEWsxClXi-l7i8300GBwfkFvL9HV'}
dbname = 'homework3'

## DATA SET CANZONI
total= json.loads(open('tot.json', 'r').read())

collection = 'songs_collections'

list_provvisoria=[]
for key in total.keys():
    chiave={}
    chiave[key]=total[key]
    list_provvisoria.append(chiave)

for i in range(0, len(list_provvisoria),10000):
    url = 'https://api.mlab.com/api/1/databases/' + dbname + '/collections/' + collection
    headers = {'content-type': 'application/json'}
    data = json.dumps(list_provvisoria[i: i+10000])
    response = requests.post(url, data=data, params=params, headers=headers)
    time.sleep(3)

### POSTING LIST  (viene caricata come un unico dizionario!!)
list_tf= json.loads(open('list_tf.json', 'r').read())
collection = 'posting_list'


list_provvisoria=[]
for key in list_tf.keys():
    chiave={}
    chiave[key]=list_tf[key]
    list_provvisoria.append(chiave)


for i in range(0, len(list_provvisoria),10000):
    url = 'https://api.mlab.com/api/1/databases/' + dbname + '/collections/' + collection
    headers = {'content-type': 'application/json'}
    data = json.dumps(list_provvisoria[i: i+10000])
    response = requests.post(url, data=data, params=params, headers=headers)
    time.sleep(3)
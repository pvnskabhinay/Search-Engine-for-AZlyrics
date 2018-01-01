# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 07:50:51 2017

@author: alber
"""

import pandas as pd
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import numpy as np
from collections import defaultdict
import json
import matplotlib.pyplot as plt
import string


############################# SONG WORDS --> rivedere codice e cambiare il nome variabile!

data_table = pd.read_csv('lyrics_dataset.csv', delimiter = '\t')
#data_table = pd.read_csv('try.csv', delimiter = '\t')


###############################################################
###############################################################
###############################################################
############### ARTIST WITH MOST SONGS ########################
###############################################################
###############################################################


artists_dict = {}
seen_artists = set()

for artist in data_table['Artist'].values:
    if str(artist) not in seen_artists:
        artists_dict[str(artist)] = 1
        seen_artists.add(str(artist))
    else:
        artists_dict[str(artist)] += 1

most_song = []

for artist in artists_dict.keys():
    if artists_dict[artist] > 200:
        most_song.append([artist, artists_dict[artist]])
        
most_song.sort(key=lambda x: x[1], reverse = True)

data= pd.DataFrame(most_song, columns=['Artist name', 'frequency'])
data.plot(kind='bar', x='Artist name')
plt.show()

table = pd.DataFrame(most_song)
table.to_csv('most_song.csv', sep='\t', encoding='utf-8')



###############################################################
###############################################################
###############################################################
############### song_with_most_word ###########################
###############################################################
###############################################################

noStem_lyrics = {}

for line in data_table[['Title', 'Artist', 'Lyrics']].values:
    lyrics = str(line[2]).split()
    noStem_lyrics[str(line[0]), str(line[1])] = len(lyrics)
    
song_with_most_word = []

for word in noStem_lyrics.keys():
    song_with_most_word.append([word, noStem_lyrics[word]])
        
song_with_most_word.sort(key=lambda x: x[1], reverse = True)
song_with_most_word=song_with_most_word[:20]


data= pd.DataFrame(song_with_most_word, columns=['Song', 'frequency'])
data.plot(kind='bar', x='Song')
plt.show()

table = pd.DataFrame(song_with_most_word)
table.to_csv('song_with_most_word.csv', sep='\t', encoding='utf-8')



  
###############################################################
###############################################################
###############################################################
############### singer_name ###################################
###############################################################
###############################################################

def freq(document):  #restituisce il dizionario con chiave il nome della parola e valore la frequeza
    seen_word=set()
    freq={}
    for char in document:
        if char in seen_word:
            freq[char]+=1
        else:
            seen_word.add(char)
            freq[char]=1
    return(freq)

singer_name=set()

for key in testi_stemmati.keys():
    for value in testi_stemmati[key]:
        if str(value)=='Artist':
            singer_name.add(testi_stemmati[key][value])
singer_name=list(singer_name)
for i in range(len(singer_name)):
    singer_name[i]=singer_name[i].split()
singer=[]
for i in range(len(singer_name)):
    for j in range(len(singer_name[i])):
        singer.append(singer_name[i][j].lower())
            
    

stop_en = get_stop_words('english')
stop_fr = get_stop_words('french')
stop_it = get_stop_words('italian')
stop_sp = get_stop_words('spanish')
stop_po = get_stop_words('portuguese')
stop_da = get_stop_words('german')
stop_ru = get_stop_words('russian')
all_stop = stop_sp + stop_it + stop_en + stop_fr + stop_po + stop_da # need stopwords for all song languages
all_stop = set(all_stop)    

for word in singer:
    if word in all_stop:
        singer.remove(word)
    if str(word) == 'band' or str(word) == '&' or str(word) == 'the':
        singer.remove(word)


singer_count=freq(singer)

import operator
sorted_singer = sorted(singer_count.items(), key=operator.itemgetter(1), reverse=True)
sorted_singer_10=sorted_singer[:10]

text=[]
i=0
for word in sorted_singer[:10]:
    for key in artists_dict.keys():
        if word[0] in str(key).lower():
            i+=1
            text.append([key, artists_dict[key]])
            print(key)
            print(artists_dict[key])
            print('-----------------')
            

table = pd.DataFrame(sorted_singer_10)
table.to_csv('sorted_singer_10.csv', sep='\t', encoding='utf-8')
table = pd.DataFrame(text)
table.to_csv('text.csv', sep='\t', encoding='utf-8')

            
### calcolando la correlazione
vett_nomi=[]
vett_song=[]
for word in sorted_singer[:10]:
    for key in artists_dict.keys():
        if word[0] in str(key).lower():
            vett_nomi.append(key)
            vett_song.append(artists_dict[key])



###############################################################
###############################################################
###############################################################
############### most_common_words #############################
###############################################################
###############################################################

word_common_dict={}
for key in list_tf.keys():
    try:
        word_common_dict[key]=sum(list_tf[key].values())
    except:
        TypeError
        
    
most_word=[]
for word in word_common_dict.keys():
     most_word.append([word, word_common_dict[word]])
        
most_word.sort(key=lambda x: x[1], reverse = True)

most_word_20=most_word[:20]

data= pd.DataFrame(most_word_20, columns=['Word', 'frequency'])
data.plot(kind='bar', x='Word')
plt.show()

table = pd.DataFrame(most_word_20)
table.to_csv('most_word_20.csv', sep='\t', encoding='utf-8')
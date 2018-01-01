# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 12:15:39 2017

@author: alber
"""
import re
from bs4 import BeautifulSoup
import time
import requests

u = open('all_songs.txt','r',encoding='utf8')

song_set = set()
for line in u:
    song_set.add(line.strip('\n')) #fatto il set
u.close()

sorted_song = sorted(list(song_set))

w = open('song_final.csv','w',encoding='utf8')

# tab separated file
w.write('Title')
w.write('\t')
w.write('Artist')
w.write('\t')
w.write('Url')
w.write('\t')
w.write('Lyrics')
w.write('\n')

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

i = 0
for link in sorted_song:
    time.sleep(3)
    url = 'https://www.azlyrics.com/'+link
    cnt = requests.get(url, headers = headers)
    while cnt.status_code != 200:
        time.sleep(3)
        cnt = requests.get(link)
        
    soup = BeautifulSoup(cnt.text, "lxml")

    # Title 
    w.write(soup.title.text.split(" Lyrics - ")[1])    
    w.write('\t')
    
    # Artist    
    w.write(soup.title.text.split(" Lyrics - ")[0])
    w.write('\t')

    # Url
    w.write(url)
    w.write('\t')
    
    #Lyrics
    lyrics_tag = soup.find_all("div", attrs= {'class':None, 'id':None})
    lyrics = [tag.getText() for tag in lyrics_tag]
    lyrics = '\n'.join(lyrics)
    lyrics = re.sub("\r\n","", lyrics)
    lyrics = re.sub("\r","", lyrics)
    lyrics = re.sub("\n","", lyrics)
    lyrics = re.sub("\t"," ", lyrics)
    w.write(lyrics)
    w.write('\n')
    
    sorted_song.remove(link)
    i += 1
    print(i)
    
    
w.close()
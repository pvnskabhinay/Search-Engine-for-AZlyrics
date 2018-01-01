# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 18:29:57 2017

@author: alber
"""
import requests
from bs4 import BeautifulSoup
import time


g = open('all_artists.txt','r',encoding='utf8')

artists_set = set()
for line in g:
    artists_set.add(line.strip('\n')) #fatto il set
g.close()

sorted_artists = sorted(list(artists_set))

h = open('all_songs.txt','w')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
           
for link in sorted_artists:
    time.sleep(1)
    url = 'https://www.azlyrics.com/'+link
    cnt = requests.get(url, headers = headers)
    while cnt.status_code != 200: # until connection error
        time.sleep(2)
        # all song letter by letter
        cnt = requests.get(url, headers = headers)
        
    soup = BeautifulSoup(cnt.text, "lxml")
    # xml page as .txt
    for line in soup.find_all('a'):
        if type(line.get('href')) == str: #got problem with 'Nonetype'
            if (line.get('href').startswith('../lyrics/')):
                song_link = line.get('href') + '\n'
                #if song_link:
                h.write(song_link[3:])
                print(song_link[3:])
    
    sorted_artists.remove(link)

h.close()
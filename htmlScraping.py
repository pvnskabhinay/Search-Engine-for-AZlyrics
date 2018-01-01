# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 14:45:48 2017

@author: alber
"""

from bs4 import BeautifulSoup
import os
import re
import sys

sys.setrecursionlimit(2000)
i = 0
html_toAvoid = ['archive.html', 'contact_us.php.html', 'lyrics_submit.php.html', 'search.php.html']

w = open('lyrics_dataset_30K.csv', 'w', encoding='utf8')

# tab separated file
w.write('Title')
w.write('\t')
w.write('Artist')
w.write('\t')
w.write('Url')
w.write('\t')
w.write('Lyrics')
w.write('\n')


#C:\Users\alber\Desktop\cici
dir_html = '/Users/alber/Desktop/lyrics_collection/'

for html in os.listdir(dir_html):
    if html not in html_toAvoid:
        print(html)
        soup = BeautifulSoup(open(dir_html+html, encoding = 'utf8'), 'html.parser')
        
        # Title
        w.write(soup.title.text.split(" Lyrics - ")[0])    
        w.write('\t')
        
        # Artist    
        w.write(soup.title.text.split(" Lyrics - ")[1])
        w.write('\t')
    
        # Url
        w.write(html)
        w.write('\t')
        
        # Lyrics
        lyrics = soup.find_all('div', attrs= {'class':'dn', 'id':'content_h'})
        lyrics = str(lyrics).replace("<br>", ' ')
        lyrics = lyrics.replace('</br>', '')
        lyrics = lyrics.replace('</div>]', '')
        lyrics = lyrics.replace('[<div class="dn" id="content_h">', '')
        lyrics = re.sub("\r\n","" , lyrics)
        lyrics = re.sub("\r","", lyrics)
        lyrics = re.sub("\n"," ", lyrics)
        lyrics = re.sub("\t"," ", lyrics)
        w.write(lyrics)
        w.write('\n')
        
        i += 1
        print(i)

w.close()
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 15:46:49 2017

@author: alber
"""

import requests
from bs4 import BeautifulSoup
import string
import time

f = open('all_artists.txt','w')
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# take all links for artists from A to Z     
for letter in string.ascii_lowercase:
    time.sleep(1)
    url = "https://www.azlyrics.com/"+letter+".html"
    cnt = requests.get(url, headers = headers)
    while cnt.status_code != 200: # until connection error
        time.sleep(2)
        # all artist letter by letter
        cnt = requests.get(url, headers = headers)
            
    soup = BeautifulSoup(cnt.text, "lxml")
    # xml page as .txt
    for line in soup.find_all('a'):
        href = line.get('href')
        if 'www' not in href:
            f.write(href + '\n')
    print(soup.title)

# take all links for all other artists(# page)   
url = "https://www.azlyrics.com/19.html"
cnt = requests.get(url, headers = headers)
while cnt.status_code != 200: # until connection error
    time.sleep(2)
    # all artist letter by letter
    cnt = requests.get(url, headers = headers)
        
soup = BeautifulSoup(cnt.text, "lxml")
# xml page as .txt
for line in soup.find_all('a'):
    href = line.get('href')
    if 'www' not in href:
        f.write(href + '\n')

print(soup.title)

f.close()

